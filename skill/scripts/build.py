"""
Diataxis documentation build pipeline.

Reads diataxis.toml, converts markdown to HTML via pandoc, generates landing
pages and navigation, exports marimo exercises to self-contained WASM HTML
bundles, and inserts iframe references pointing at those bundles.

Usage:
    diataxis build
    diataxis serve
    diataxis serve-only
    diataxis publish
    diataxis build -d path/to/diataxis
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import textwrap
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import NoReturn

STATIC_PORT = 8000

QUADRANT_META: dict[str, dict[str, str]] = {
    "tutorials": {
        "label": "Tutorials",
        "description": "Learn by doing — guided lessons that take you through a topic step by step.",
    },
    "howto": {
        "label": "How-to Guides",
        "description": "Practical directions for accomplishing specific tasks.",
    },
    "reference": {
        "label": "Reference",
        "description": "Technical descriptions and specifications.",
    },
    "explanation": {
        "label": "Explanation",
        "description": "Background, context, and deeper understanding.",
    },
}
QUADRANT_DIRS = tuple(QUADRANT_META.keys())


def humanize(stem: str) -> str:
    """Turn a file stem into a display title ('basic-ops' → 'Basic Ops')."""
    return stem.replace("-", " ").replace("_", " ").title()


def fail(msg: str, code: int = 1) -> NoReturn:
    """Write *msg* to stderr and exit."""
    print(msg, file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Port utilities
# ---------------------------------------------------------------------------


def find_available_port(start: int) -> int:
    """Find an available port starting from *start*.

    Probes by binding and releasing. There is a small race window between the
    release and the caller's subsequent bind; this is acceptable for local dev.
    """
    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                port += 1
    fail(f"Error: no available port in range {start}-{start + 99}")


# ---------------------------------------------------------------------------
# Structure reading
# ---------------------------------------------------------------------------


def read_structure(diataxis_dir: Path) -> dict:
    toml_path = diataxis_dir / "diataxis.toml"
    if not toml_path.exists():
        fail(f"Error: {toml_path} not found")
    with open(toml_path, "rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Exercise normalization
# ---------------------------------------------------------------------------


DEFAULT_EXERCISE_HEIGHT = 600


def normalize_exercise(ex: str | dict) -> dict:
    """Normalize an exercise entry to {file, title, height}.

    Accepts either a plain string (path) or a table with `file` plus optional
    `title` and `height` overrides.
    """
    if isinstance(ex, str):
        file = ex
        title = None
        height = None
    else:
        file = ex["file"]
        title = ex.get("title")
        height = ex.get("height")
    stem = Path(file).stem
    return {
        "file": file,
        "stem": stem,
        "title": title or humanize(stem),
        "height": height or DEFAULT_EXERCISE_HEIGHT,
    }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def iter_entries(structure: dict):
    """Yield (topic_slug, quadrant, entry) for every defined quadrant entry."""
    for topic_slug, topic in structure.get("topics", {}).items():
        for quadrant in QUADRANT_DIRS:
            entry = topic.get(quadrant)
            if entry is not None:
                yield topic_slug, quadrant, entry


def validate(structure: dict, diataxis_dir: Path) -> tuple[list[str], list[str]]:
    """Check that referenced files exist and exercise stems don't collide.

    Returns (errors, warnings). Errors fail the build; warnings don't.
    Missing referenced content or exercise files would otherwise produce a
    silently broken site.
    """
    errors: list[str] = []
    warnings: list[str] = []
    seen_stems: dict[str, str] = {}  # stem -> first file that claimed it

    for topic_slug, quadrant, entry in iter_entries(structure):
        if not (diataxis_dir / entry["file"]).exists():
            errors.append(
                f"Missing content: {entry['file']} (topic: {topic_slug}, quadrant: {quadrant})"
            )
        for ex in entry.get("exercises", []):
            ex_info = normalize_exercise(ex)
            if not (diataxis_dir / ex_info["file"]).exists():
                errors.append(
                    f"Missing exercise: {ex_info['file']} (topic: {topic_slug})"
                )
            prior = seen_stems.get(ex_info["stem"])
            if prior is not None and prior != ex_info["file"]:
                errors.append(
                    f"Exercise stem collision: {prior!r} and {ex_info['file']!r} "
                    f"both export to exercises/{ex_info['stem']}/"
                )
            else:
                seen_stems[ex_info["stem"]] = ex_info["file"]

    return errors, warnings


# ---------------------------------------------------------------------------
# Landing page generation
# ---------------------------------------------------------------------------


def generate_landing_page(quadrant: str, structure: dict, diataxis_dir: Path) -> None:
    """Generate an index.md for a quadrant directory from the structure."""
    quadrant_dir = diataxis_dir / quadrant
    quadrant_dir.mkdir(parents=True, exist_ok=True)

    meta = QUADRANT_META[quadrant]
    lines = [
        f"# {meta['label']}",
        "",
        meta["description"],
        "",
    ]

    topics = structure.get("topics", {})
    sorted_topics = sorted(
        topics.items(),
        key=lambda item: item[1].get("order", 999),
    )

    for _, topic in sorted_topics:
        entry = topic.get(quadrant)
        if entry is None:
            continue
        file_rel = Path(entry["file"]).with_suffix(".html")
        link_target = file_rel.name
        covers = entry.get("covers", [])
        covers_text = ", ".join(covers[:3])
        if len(covers) > 3:
            covers_text += ", ..."

        lines.append(f"## {topic['title']}")
        lines.append("")
        lines.append(f"[{topic['title']}]({link_target})")
        if covers_text:
            lines.append(f": {covers_text}")
        lines.append("")

    index_path = quadrant_dir / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pandoc conversion
# ---------------------------------------------------------------------------


SKILL_ASSETS = Path(__file__).parent.parent / "assets"


def get_pandoc_template(diataxis_dir: Path) -> Path:
    """Return the template path — project-local override or bundled default."""
    local = diataxis_dir / "_templates" / "page.html"
    if local.exists():
        return local
    return SKILL_ASSETS / "template.html"


MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def has_mmdc() -> bool:
    """Check if the mermaid CLI is available."""
    return shutil.which("mmdc") is not None


def prerender_mermaid(md_content: str, svg_dir: Path, name_prefix: str, asset_prefix: str = "") -> str:
    """Replace ```mermaid blocks with rendered SVG image references.

    Each block is written to a temp file, rendered with mmdc, and the
    resulting SVG is saved to svg_dir. The markdown is returned with
    the code block replaced by an image reference pointing to the SVG.

    asset_prefix is prepended to the image path (e.g., "../" for files
    in subdirectories).
    """
    if not MERMAID_BLOCK.search(md_content):
        return md_content

    if not has_mmdc():
        print("  WARNING: mermaid blocks found but mmdc is not installed", file=sys.stderr)
        return md_content

    svg_dir.mkdir(parents=True, exist_ok=True)
    counter = 0

    def render_block(match: re.Match) -> str:
        nonlocal counter
        counter += 1
        mermaid_src = match.group(1)
        svg_name = f"{name_prefix}-mermaid-{counter}.svg"
        svg_path = svg_dir / svg_name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
            f.write(mermaid_src)
            mmd_path = f.name

        try:
            result = subprocess.run(
                ["mmdc", "-i", mmd_path, "-o", str(svg_path), "-b", "transparent"],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  WARNING: mmdc failed for block {counter}: {result.stderr}", file=sys.stderr)
                return match.group(0)
        finally:
            Path(mmd_path).unlink(missing_ok=True)

        return f'![diagram]({asset_prefix}assets/mermaid/{svg_name})'

    return MERMAID_BLOCK.sub(render_block, md_content)


def convert_markdown(
    md_path: Path,
    html_path: Path,
    title: str,
    template: Path,
    build_dir: Path,
    *,
    quadrant: str | None = None,
    cssroot: str = "",
) -> None:
    """Convert a single markdown file to HTML via pandoc.

    If the markdown contains ```mermaid blocks, they are pre-rendered to SVG
    and saved in build_dir/assets/mermaid/ before pandoc runs.
    """
    html_path.parent.mkdir(parents=True, exist_ok=True)

    md_content = md_path.read_text(encoding="utf-8")
    svg_dir = build_dir / "assets" / "mermaid"
    processed = prerender_mermaid(md_content, svg_dir, md_path.stem, asset_prefix=cssroot)

    pandoc_input: Path | str
    tmp_path: str | None = None
    if processed != md_content:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", encoding="utf-8", delete=False,
        ) as f:
            f.write(processed)
            tmp_path = f.name
        pandoc_input = tmp_path
    else:
        pandoc_input = md_path

    try:
        cmd = [
            "pandoc", str(pandoc_input),
            "--from", "markdown",
            "--to", "html5",
            "--standalone",
            "--mathjax",
            "--template", str(template),
            "--metadata", f"title={title}",
            "--metadata", f"cssroot={cssroot}",
            "--toc",
            "--toc-depth=2",
            "-o", str(html_path),
        ]
        if quadrant:
            cmd.extend(["--metadata", f"quadrant={quadrant}"])

        result = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if tmp_path is not None:
            Path(tmp_path).unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"  pandoc error for {md_path}: {result.stderr}", file=sys.stderr)
    else:
        content = html_path.read_text(encoding="utf-8")
        content = re.sub(r'href="([^"]*?)\.md"', r'href="\1.html"', content)
        html_path.write_text(content, encoding="utf-8")
        print(f"  {md_path.name} -> {html_path.name}")


# ---------------------------------------------------------------------------
# Marimo WASM export + iframe insertion
# ---------------------------------------------------------------------------


def export_exercise_wasm(src_py: Path, out_dir: Path) -> bool:
    """Export a marimo notebook as a self-contained WASM HTML bundle.

    Skips the export when `out_dir/index.html` already exists and is newer
    than `src_py`, since `marimo export html-wasm` produces a multi-MB bundle
    per exercise and is the slowest step in the build.
    """
    bundle_index = out_dir / "index.html"
    if bundle_index.exists() and bundle_index.stat().st_mtime >= src_py.stat().st_mtime:
        print(f"  {src_py.name} -> exercises/{out_dir.name}/ (cached)")
        return True

    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "marimo", "export", "html-wasm",
        str(src_py),
        "-o", str(out_dir),
        "--mode", "run",
        "-f",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  marimo export failed for {src_py.name}: {result.stderr}", file=sys.stderr)
        return False
    print(f"  {src_py.name} -> exercises/{out_dir.name}/")
    return True


BODY_CLOSE = re.compile(r"</body\s*>", re.IGNORECASE)


def insert_exercise_iframes(html_path: Path, exercises: list[dict], asset_prefix: str = "") -> None:
    """Append exercise iframes (pointing at WASM bundles) to an HTML file.

    `exercises` is a list of normalized exercise dicts (see normalize_exercise).
    """
    if not exercises:
        return

    iframe_blocks = []
    for ex in exercises:
        iframe_blocks.append(textwrap.dedent(f"""\
            <div class="marimo-exercise">
                <h3>Exercise: {ex['title']}</h3>
                <iframe
                    src="{asset_prefix}exercises/{ex['stem']}/index.html"
                    sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
                    width="100%"
                    height="{ex['height']}"
                    loading="lazy">
                </iframe>
            </div>
        """))

    content = html_path.read_text(encoding="utf-8")
    insertion = "\n".join(iframe_blocks)
    # Regex + count=1 instead of str.replace so a literal </body> inside a code sample doesn't misfire.
    content, replaced = BODY_CLOSE.subn(f"{insertion}\n</body>", content, count=1)
    if not replaced:
        content += "\n" + insertion + "\n"
    html_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Sidebar generation
# ---------------------------------------------------------------------------


def generate_sidebar_html(structure: dict) -> str:
    """Build the sidebar navigation HTML from the structure document."""
    project = structure.get("project", {})
    name = project.get("name", "Documentation")

    topics = structure.get("topics", {})
    sorted_topics = sorted(
        topics.items(),
        key=lambda item: item[1].get("order", 999),
    )

    lines = [f'<a class="site-title" href="index.html">{name}</a>']

    for quadrant in QUADRANT_DIRS:
        entries = []
        for _, topic in sorted_topics:
            entry = topic.get(quadrant)
            if entry is None:
                continue
            file_html = Path(entry["file"]).with_suffix(".html").name
            entries.append((topic["title"], f"{quadrant}/{file_html}"))

        if not entries:
            continue

        lines.append(f'<div class="nav-section {quadrant}">')
        lines.append(f'  <div class="nav-section-title">{QUADRANT_META[quadrant]["label"]}</div>')
        lines.append("  <ul>")
        for title, href in entries:
            lines.append(f'    <li><a href="{href}">{title}</a></li>')
        lines.append("  </ul>")
        lines.append("</div>")

    return "\n".join(lines)


# Matches only relative site-internal hrefs — leaves absolute URLs and fragments alone.
RELATIVE_HREF = re.compile(r'href="(?![a-z][a-z0-9+.-]*:|/|#)')


def inject_sidebar(html_path: Path, sidebar_html: str, current_href: str) -> None:
    """Replace the sidebar placeholder and mark the active link."""
    content = html_path.read_text(encoding="utf-8")

    if html_path.parent.name in QUADRANT_DIRS:
        adjusted = RELATIVE_HREF.sub('href="../', sidebar_html)
    else:
        adjusted = sidebar_html

    if current_href:
        adjusted = adjusted.replace(
            f'href="{current_href}"',
            f'href="{current_href}" class="active"',
        )

    content = content.replace(
        "<!-- Sidebar content is injected by the build script -->",
        adjusted,
    )
    html_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Build orchestration
# ---------------------------------------------------------------------------


def collect_exercises(structure: dict) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """Return (per-file exercises, stem-keyed unique exercises) from a structure."""
    per_file: dict[str, list[dict]] = {}
    by_stem: dict[str, dict] = {}
    for _, _, entry in iter_entries(structure):
        normalized = [normalize_exercise(e) for e in entry.get("exercises", [])]
        if not normalized:
            continue
        per_file[entry["file"]] = normalized
        for n in normalized:
            by_stem[n["stem"]] = n
    return per_file, by_stem


def clean_build_dir(build_dir: Path) -> None:
    """Empty *build_dir* while preserving ``exercises/`` for WASM-export caching."""
    if not build_dir.exists():
        build_dir.mkdir()
        return
    for child in build_dir.iterdir():
        if child.name == "exercises":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def build(diataxis_dir: Path) -> None:
    """Run the full build pipeline."""
    print(f"Building from {diataxis_dir}")

    structure = read_structure(diataxis_dir)

    errors, warnings = validate(structure, diataxis_dir)
    for w in warnings:
        print(f"  WARNING: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        fail(
            f"\n{len(errors)} validation error(s). "
            "Fix diataxis.toml or the missing files and re-run."
        )

    file_exercises, all_exercises = collect_exercises(structure)

    if all_exercises and shutil.which("marimo") is None:
        fail(
            "Error: `marimo` is not on PATH but the project references exercises. "
            "Install it (e.g., `uv sync`) and try again."
        )

    build_dir = diataxis_dir / "_build"
    clean_build_dir(build_dir)

    assets_dest = build_dir / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    for asset_file in SKILL_ASSETS.glob("*.css"):
        shutil.copy2(asset_file, assets_dest / asset_file.name)
    print("Copied standard assets.")

    project_assets = diataxis_dir / "_assets"
    if project_assets.exists():
        shutil.copytree(project_assets, assets_dest, dirs_exist_ok=True)
        print("Copied project assets.")

    print("Generating landing pages...")
    for quadrant in QUADRANT_DIRS:
        generate_landing_page(quadrant, structure, diataxis_dir)

    if all_exercises:
        # Each export shells out to marimo and is CPU/IO-bound — thread pool works fine.
        print("Exporting exercises to WASM...")
        with ThreadPoolExecutor(max_workers=min(len(all_exercises), os.cpu_count() or 4)) as pool:
            futures = [
                pool.submit(
                    export_exercise_wasm,
                    diataxis_dir / ex["file"],
                    build_dir / "exercises" / stem,
                )
                for stem, ex in sorted(all_exercises.items())
            ]
            for fut in as_completed(futures):
                fut.result()

    sidebar_html = generate_sidebar_html(structure)

    template = get_pandoc_template(diataxis_dir)
    print("Converting markdown to HTML...")

    home_md = diataxis_dir / "index.md"
    if home_md.exists():
        home_html = build_dir / "index.html"
        convert_markdown(home_md, home_html, structure.get("project", {}).get("name", "Home"), template, build_dir)
        inject_sidebar(home_html, sidebar_html, "")

    for quadrant in QUADRANT_DIRS:
        quadrant_src = diataxis_dir / quadrant
        if not quadrant_src.exists():
            continue
        for md_file in sorted(quadrant_src.glob("*.md")):
            rel = md_file.relative_to(diataxis_dir)
            html_rel = rel.with_suffix(".html")
            html_path = build_dir / html_rel
            cssroot = "../"
            convert_markdown(
                md_file, html_path, humanize(md_file.stem), template, build_dir,
                quadrant=quadrant,
                cssroot=cssroot,
            )

            inject_sidebar(html_path, sidebar_html, f"{quadrant}/{html_rel.name}")

            rel_str = str(rel)
            if rel_str in file_exercises:
                insert_exercise_iframes(html_path, file_exercises[rel_str], asset_prefix=cssroot)

    print(f"Build complete: {build_dir}")
    print(f"Open {build_dir}/index.html in your browser, or run 'diataxis serve' to start a local server.")


# ---------------------------------------------------------------------------
# Serve
# ---------------------------------------------------------------------------


def serve(diataxis_dir: Path, *, rebuild: bool = True) -> None:
    """Start a local static server for _build/. Exercises run in-browser via WASM."""
    if rebuild:
        build(diataxis_dir)

    build_dir = diataxis_dir / "_build"
    if not build_dir.exists():
        fail("Build directory not found. Run 'diataxis build' first.")

    static_port = find_available_port(STATIC_PORT)
    print(f"Starting static server on port {static_port}...")
    print(f"Open http://localhost:{static_port} in your browser.")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir), **kwargs)

    server = http.server.HTTPServer(("localhost", static_port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()


# ---------------------------------------------------------------------------
# Publish
# ---------------------------------------------------------------------------


SITES_MANIFEST = ".diataxis-meta.json"


def slugify(value: str) -> str:
    """Lowercase, replace runs of non-alphanumerics with hyphens, trim ends."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError(f"cannot slugify {value!r}")
    return slug


def publish(diataxis_dir: Path, sites_dir: Path) -> None:
    """Build the site, copy it to sites_dir/<slug>/, and regenerate the top-level index."""
    structure = read_structure(diataxis_dir)
    project = structure.get("project", {})
    name = project.get("name")
    if not name:
        fail("Error: project.name is required in diataxis.toml")

    build(diataxis_dir)
    build_dir = diataxis_dir / "_build"

    slug = slugify(name)
    sites_dir.mkdir(parents=True, exist_ok=True)
    dest = sites_dir / slug

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(build_dir, dest)
    print(f"Published {name} → {dest}")

    manifest = {
        "name": name,
        "slug": slug,
        "description": project.get("description", ""),
    }
    (dest / SITES_MANIFEST).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    generate_sites_index(sites_dir)


def generate_sites_index(sites_dir: Path) -> None:
    """Render sites_dir/index.html from the Jinja2 template, scanning published projects."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    projects = []
    for meta_file in sorted(sites_dir.glob(f"*/{SITES_MANIFEST}")):
        try:
            projects.append(json.loads(meta_file.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  WARNING: skipping {meta_file}: {exc}", file=sys.stderr)

    env = Environment(
        loader=FileSystemLoader(str(SKILL_ASSETS)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    template = env.get_template("sites-index.html.j2")
    html = template.render(projects=projects)

    index_path = sites_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"Updated {index_path} ({len(projects)} project{'s' if len(projects) != 1 else ''})")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    from importlib.metadata import version
    pkg_version = version("skill-diataxis")

    parser = argparse.ArgumentParser(description="Diataxis documentation build pipeline")
    parser.add_argument("-v", "--version", action="version", version=f"diataxis {pkg_version}")
    sub = parser.add_subparsers(dest="command")
    for name, help_text in [
        ("build", "Build HTML from markdown sources"),
        ("serve", "Build and start a local static server"),
        ("serve-only", "Start the static server without rebuilding"),
        ("publish", "Copy the built site to ~/Sites/<project-slug>/ and refresh ~/Sites/index.html"),
    ]:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("-d", "--dir", default="diataxis",
                        help="Path to the diataxis directory (default: ./diataxis)")
        if name == "publish":
            sp.add_argument(
                "--sites-dir",
                default=str(Path.home() / "Sites"),
                help="Target sites directory (default: ~/Sites)",
            )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    diataxis_dir = Path(args.dir).resolve()

    if args.command == "build":
        build(diataxis_dir)
    elif args.command == "serve":
        serve(diataxis_dir)
    elif args.command == "serve-only":
        serve(diataxis_dir, rebuild=False)
    elif args.command == "publish":
        publish(diataxis_dir, Path(args.sites_dir).expanduser().resolve())


if __name__ == "__main__":
    main()
