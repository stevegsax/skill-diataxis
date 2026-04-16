"""
Diataxis documentation build pipeline.

Reads diataxis.toml, converts markdown to HTML via pandoc, generates landing
pages and navigation, and inserts marimo iframe references.

Usage:
    diataxis build
    diataxis serve
    diataxis serve-only
    diataxis exercises
    diataxis publish
    diataxis build -d path/to/diataxis
"""

from __future__ import annotations

import argparse
import http.server
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import textwrap
import tomllib
from pathlib import Path

QUADRANT_DIRS = ("tutorials", "howto", "reference", "explanation")
MARIMO_PORT = 2718
STATIC_PORT = 8000


# ---------------------------------------------------------------------------
# Port utilities
# ---------------------------------------------------------------------------


def find_available_port(start: int) -> int:
    """Find an available port starting from *start*."""
    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                port += 1
    print(f"Error: no available port in range {start}-{start + 99}", file=sys.stderr)
    sys.exit(1)


def read_built_marimo_port(diataxis_dir: Path) -> int:
    """Read the marimo port from the generated exercise script."""
    script = diataxis_dir / "_serve_exercises.py"
    if not script.exists():
        return MARIMO_PORT
    match = re.search(r"port=(\d+)", script.read_text(encoding="utf-8"))
    return int(match.group(1)) if match else MARIMO_PORT


# ---------------------------------------------------------------------------
# Structure reading
# ---------------------------------------------------------------------------


def read_structure(diataxis_dir: Path) -> dict:
    toml_path = diataxis_dir / "diataxis.toml"
    if not toml_path.exists():
        print(f"Error: {toml_path} not found", file=sys.stderr)
        sys.exit(1)
    with open(toml_path, "rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(structure: dict, diataxis_dir: Path) -> list[str]:
    """Check that referenced files exist. Returns list of warnings."""
    warnings = []
    topics = structure.get("topics", {})
    for topic_slug, topic in topics.items():
        for quadrant in QUADRANT_DIRS:
            entry = topic.get(quadrant)
            if entry is None:
                continue
            file_path = diataxis_dir / entry["file"]
            if not file_path.exists():
                warnings.append(f"Missing: {entry['file']} (topic: {topic_slug}, quadrant: {quadrant})")
            for ex in entry.get("exercises", []):
                ex_path = diataxis_dir / ex
                if not ex_path.exists():
                    warnings.append(f"Missing exercise: {ex} (topic: {topic_slug})")
    return warnings


# ---------------------------------------------------------------------------
# Landing page generation
# ---------------------------------------------------------------------------


def generate_landing_page(quadrant: str, structure: dict, diataxis_dir: Path) -> None:
    """Generate an index.md for a quadrant directory from the structure."""
    quadrant_dir = diataxis_dir / quadrant
    quadrant_dir.mkdir(parents=True, exist_ok=True)

    titles = {
        "tutorials": "Tutorials",
        "howto": "How-to Guides",
        "reference": "Reference",
        "explanation": "Explanation",
    }
    descriptions = {
        "tutorials": "Learn by doing — guided lessons that take you through a topic step by step.",
        "howto": "Practical directions for accomplishing specific tasks.",
        "reference": "Technical descriptions and specifications.",
        "explanation": "Background, context, and deeper understanding.",
    }

    lines = [
        f"# {titles[quadrant]}",
        "",
        descriptions[quadrant],
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
        # Link target is just the filename since we're in the same directory
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


def generate_home_page(structure: dict, diataxis_dir: Path) -> None:
    """Generate the root index.md for the documentation site."""
    project = structure.get("project", {})
    name = project.get("name", "Documentation")
    description = project.get("description", "")
    purpose = project.get("purpose", "")
    audience = project.get("audience", "")
    introduction = project.get("introduction", "")

    lines = [
        f"# {name}",
        "",
    ]
    if purpose:
        lines.extend([purpose.strip(), ""])
    elif description:
        lines.extend([description, ""])

    if audience:
        lines.extend([f"**Audience**: {audience}", ""])

    if introduction:
        lines.extend([introduction.strip(), ""])

    lines.extend([
        "## Sections",
        "",
        "- [Tutorials](tutorials/index.html) — Learn by doing",
        "- [How-to Guides](howto/index.html) — Accomplish specific tasks",
        "- [Reference](reference/index.html) — Technical descriptions",
        "- [Explanation](explanation/index.html) — Background and context",
        "",
    ])

    index_path = diataxis_dir / "index.md"
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
                return match.group(0)  # Leave the original block
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

    # Pre-render mermaid blocks if present
    md_content = md_path.read_text(encoding="utf-8")
    svg_dir = build_dir / "assets" / "mermaid"
    processed = prerender_mermaid(md_content, svg_dir, md_path.stem, asset_prefix=cssroot)

    if processed != md_content:
        # Write processed markdown to a temp file for pandoc
        tmp_md = md_path.with_suffix(".tmp.md")
        tmp_md.write_text(processed, encoding="utf-8")
        pandoc_input = tmp_md
    else:
        pandoc_input = md_path
        tmp_md = None

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

    # Clean up temp file
    if tmp_md is not None:
        tmp_md.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"  pandoc error for {md_path}: {result.stderr}", file=sys.stderr)
    else:
        # Pandoc preserves .md extensions in href attributes — convert to .html
        content = html_path.read_text(encoding="utf-8")
        content = re.sub(r'href="([^"]*?)\.md"', r'href="\1.html"', content)
        html_path.write_text(content, encoding="utf-8")
        print(f"  {md_path.name} -> {html_path.name}")


# ---------------------------------------------------------------------------
# Marimo iframe insertion
# ---------------------------------------------------------------------------


def collect_exercises(structure: dict) -> dict[str, str]:
    """Return a mapping of exercise file path -> mount path for marimo."""
    exercises = {}
    topics = structure.get("topics", {})
    for topic in topics.values():
        for quadrant in QUADRANT_DIRS:
            entry = topic.get(quadrant)
            if entry is None:
                continue
            for ex in entry.get("exercises", []):
                # Mount at root level to avoid double-prefix redirect
                stem = Path(ex).stem
                exercises[ex] = f"/{stem}"
    return exercises


def insert_exercise_iframes(html_path: Path, exercises: list[str], marimo_port: int = MARIMO_PORT) -> None:
    """Append exercise iframes to an HTML file."""
    if not exercises:
        return

    iframe_blocks = []
    for ex in exercises:
        stem = Path(ex).stem
        iframe_blocks.append(textwrap.dedent(f"""\
            <div class="marimo-exercise">
                <h3>Exercise: {stem.replace('-', ' ').replace('_', ' ').title()}</h3>
                <p class="exercise-server-note">Requires exercise server — run <code>diataxis exercises</code></p>
                <iframe
                    src="http://localhost:{marimo_port}/{stem}"
                    sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
                    width="100%"
                    height="600"
                    loading="lazy">
                </iframe>
            </div>
        """))

    content = html_path.read_text(encoding="utf-8")
    # Insert before closing </body> tag
    insertion = "\n".join(iframe_blocks)
    content = content.replace("</body>", f"{insertion}\n</body>")
    html_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Sidebar generation
# ---------------------------------------------------------------------------


def generate_sidebar_html(structure: dict) -> str:
    """Build the sidebar navigation HTML from the structure document."""
    project = structure.get("project", {})
    name = project.get("name", "Documentation")

    section_labels = {
        "tutorials": "Tutorials",
        "howto": "How-to Guides",
        "reference": "Reference",
        "explanation": "Explanation",
    }

    topics = structure.get("topics", {})
    sorted_topics = sorted(
        topics.items(),
        key=lambda item: item[1].get("order", 999),
    )

    lines = [f'<a class="site-title" href="index.html">{name}</a>']

    for quadrant in QUADRANT_DIRS:
        # Collect files for this quadrant
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
        lines.append(f'  <div class="nav-section-title">{section_labels[quadrant]}</div>')
        lines.append("  <ul>")
        for title, href in entries:
            lines.append(f'    <li><a href="{href}">{title}</a></li>')
        lines.append("  </ul>")
        lines.append("</div>")

    return "\n".join(lines)


def inject_sidebar(html_path: Path, sidebar_html: str, current_href: str) -> None:
    """Replace the sidebar placeholder and mark the active link."""
    content = html_path.read_text(encoding="utf-8")

    # Fix relative paths — files in subdirectories need ../
    if html_path.parent.name in QUADRANT_DIRS:
        adjusted = sidebar_html.replace('href="', 'href="../')
    else:
        adjusted = sidebar_html

    # Mark active link
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


def build(diataxis_dir: Path, marimo_port: int = MARIMO_PORT) -> None:
    """Run the full build pipeline."""
    print(f"Building from {diataxis_dir}")

    structure = read_structure(diataxis_dir)

    # Validate
    warnings = validate(structure, diataxis_dir)
    for w in warnings:
        print(f"  WARNING: {w}", file=sys.stderr)

    build_dir = diataxis_dir / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Copy standard assets from the skill bundle
    assets_dest = build_dir / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    for asset_file in SKILL_ASSETS.glob("*.css"):
        shutil.copy2(asset_file, assets_dest / asset_file.name)
    print("Copied standard assets.")

    # Copy project-specific assets on top if they exist
    project_assets = diataxis_dir / "_assets"
    if project_assets.exists():
        shutil.copytree(project_assets, assets_dest, dirs_exist_ok=True)
        print("Copied project assets.")

    # Generate landing pages
    print("Generating landing pages...")
    generate_home_page(structure, diataxis_dir)
    for quadrant in QUADRANT_DIRS:
        generate_landing_page(quadrant, structure, diataxis_dir)

    # Collect exercises for iframe insertion
    exercise_map = collect_exercises(structure)
    # Map content file -> list of exercises
    file_exercises: dict[str, list[str]] = {}
    topics = structure.get("topics", {})
    for topic in topics.values():
        for quadrant in QUADRANT_DIRS:
            entry = topic.get(quadrant)
            if entry is None:
                continue
            if entry.get("exercises"):
                file_exercises[entry["file"]] = entry["exercises"]

    # Build sidebar HTML once
    sidebar_html = generate_sidebar_html(structure)

    # Convert all markdown files
    template = get_pandoc_template(diataxis_dir)
    print("Converting markdown to HTML...")

    # Home page
    home_md = diataxis_dir / "index.md"
    if home_md.exists():
        home_html = build_dir / "index.html"
        convert_markdown(home_md, home_html, structure.get("project", {}).get("name", "Home"), template, build_dir)
        inject_sidebar(home_html, sidebar_html, "")

    # Quadrant landing pages and content files
    for quadrant in QUADRANT_DIRS:
        quadrant_src = diataxis_dir / quadrant
        if not quadrant_src.exists():
            continue
        for md_file in sorted(quadrant_src.glob("*.md")):
            rel = md_file.relative_to(diataxis_dir)
            html_rel = rel.with_suffix(".html")
            html_path = build_dir / html_rel
            title = md_file.stem.replace("-", " ").replace("_", " ").title()

            # Determine cssroot for template — files in subdirs need ../
            cssroot = "../"
            convert_markdown(
                md_file, html_path, title, template, build_dir,
                quadrant=quadrant,
                cssroot=cssroot,
            )

            # Inject sidebar with correct relative paths
            current_href = f"{quadrant}/{html_rel.name}"
            inject_sidebar(html_path, sidebar_html, current_href)

            # Insert exercise iframes if applicable
            rel_str = str(rel)
            if rel_str in file_exercises:
                insert_exercise_iframes(html_path, file_exercises[rel_str], marimo_port)

    # Generate marimo ASGI config if there are exercises
    if exercise_map:
        generate_marimo_config(diataxis_dir, exercise_map, marimo_port)

    print(f"Build complete: {build_dir}")
    print(f"Open {build_dir}/index.html in your browser, or run 'diataxis serve' to start a local server.")


# ---------------------------------------------------------------------------
# Marimo server config generation
# ---------------------------------------------------------------------------


def generate_marimo_config(diataxis_dir: Path, exercise_map: dict[str, str], marimo_port: int = MARIMO_PORT) -> None:
    """Generate a marimo ASGI app script for serving exercises."""
    lines = [
        '"""Auto-generated marimo ASGI app for serving exercises."""',
        "",
        "import marimo",
        "",
        "app = marimo.create_asgi_app()",
        "",
    ]
    for file_path, mount_path in sorted(exercise_map.items()):
        lines.append(f'app = app.with_app(path="{mount_path}", root="./{file_path}")')

    lines.extend([
        "",
        "app = app.build()",
        "",
        'if __name__ == "__main__":',
        "    import sys",
        "    import uvicorn",
        f"    port = int(sys.argv[1]) if len(sys.argv) > 1 else {marimo_port}",
        '    uvicorn.run(app, host="localhost", port=port)',
        "",
    ])

    config_path = diataxis_dir / "_serve_exercises.py"
    config_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated marimo config: {config_path}")


# ---------------------------------------------------------------------------
# Serve
# ---------------------------------------------------------------------------


def serve(diataxis_dir: Path, *, rebuild: bool = True) -> None:
    """Start both static and marimo servers."""
    # Find available ports
    marimo_port = find_available_port(MARIMO_PORT)
    static_port = find_available_port(STATIC_PORT)
    if static_port == marimo_port:
        static_port = find_available_port(static_port + 1)

    if rebuild:
        build(diataxis_dir, marimo_port=marimo_port)

    build_dir = diataxis_dir / "_build"
    if not build_dir.exists():
        print("Build directory not found. Run 'diataxis build' first.", file=sys.stderr)
        sys.exit(1)

    exercise_script = diataxis_dir / "_serve_exercises.py"

    # Start marimo server if exercises exist
    # Use uv run so packages installed by uv are available
    marimo_proc = None
    if exercise_script.exists():
        built_port = read_built_marimo_port(diataxis_dir)
        if not rebuild and marimo_port != built_port:
            print(f"  Port {built_port} in use, exercises serving on {marimo_port}.", file=sys.stderr)
            print("  Rebuild to update exercise URLs: diataxis build", file=sys.stderr)
        print(f"Starting exercise server on port {marimo_port}...")
        marimo_proc = subprocess.Popen(
            ["uv", "run", "python", str(exercise_script), str(marimo_port)],
            cwd=str(diataxis_dir),
        )

    # Start static server
    print(f"Starting static server on port {static_port}...")
    print(f"Open http://localhost:{static_port} in your browser.")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir), **kwargs)

    try:
        server = http.server.HTTPServer(("localhost", static_port), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if marimo_proc is not None:
            marimo_proc.terminate()
            marimo_proc.wait()


def serve_exercises(diataxis_dir: Path) -> None:
    """Start only the marimo exercise server."""
    exercise_script = diataxis_dir / "_serve_exercises.py"
    if not exercise_script.exists():
        print("No exercises found. Run 'diataxis build' first.", file=sys.stderr)
        sys.exit(1)

    built_port = read_built_marimo_port(diataxis_dir)
    port = find_available_port(built_port)
    if port != built_port:
        print(f"  Port {built_port} in use, using {port}.", file=sys.stderr)
        print("  Rebuild to update exercise URLs: diataxis build", file=sys.stderr)

    print(f"Starting exercise server on port {port}...")

    try:
        subprocess.run(
            ["uv", "run", "python", str(exercise_script), str(port)],
            cwd=str(diataxis_dir),
        )
    except KeyboardInterrupt:
        print("\nShutting down...")


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
        print("Error: project.name is required in diataxis.toml", file=sys.stderr)
        sys.exit(1)

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
    dir_kwargs = {
        "flags": ["-d", "--dir"],
        "default": "diataxis",
        "help": "Path to the diataxis directory (default: ./diataxis)",
    }

    from importlib.metadata import version
    pkg_version = version("skill-diataxis")

    parser = argparse.ArgumentParser(description="Diataxis documentation build pipeline")
    parser.add_argument("-v", "--version", action="version", version=f"diataxis {pkg_version}")
    parser.add_argument(*dir_kwargs.pop("flags"), **dir_kwargs)
    sub = parser.add_subparsers(dest="command")
    for name, help_text in [
        ("build", "Build HTML from markdown sources"),
        ("serve", "Build and start local servers"),
        ("serve-only", "Start servers without rebuilding"),
        ("exercises", "Start only the exercise server (marimo)"),
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
    diataxis_dir = Path(args.dir).resolve()

    if args.command is None:
        parser.print_help()
        sys.exit(1)
    elif args.command == "build":
        build(diataxis_dir)
    elif args.command == "serve":
        serve(diataxis_dir)
    elif args.command == "serve-only":
        serve(diataxis_dir, rebuild=False)
    elif args.command == "exercises":
        serve_exercises(diataxis_dir)
    elif args.command == "publish":
        publish(diataxis_dir, Path(args.sites_dir).expanduser().resolve())


if __name__ == "__main__":
    main()
