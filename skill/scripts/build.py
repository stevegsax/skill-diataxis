"""
Diataxis documentation build pipeline.

Reads diataxis.toml, converts markdown to HTML via pandoc, generates landing
pages and navigation, and inserts marimo iframe references.

Usage:
    python -m scripts.build [diataxis-dir]
    python -m scripts.build [diataxis-dir] --serve
"""

from __future__ import annotations

import argparse
import http.server
import re
import shutil
import subprocess
import sys
import textwrap
import tomllib
from pathlib import Path

QUADRANT_DIRS = ("tutorials", "howto", "reference", "explanation")
MARIMO_PORT = 2718
STATIC_PORT = 8000


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
    audience = project.get("audience", "")

    lines = [
        f"# {name}",
        "",
        description,
        "",
    ]
    if audience:
        lines.extend([f"**Audience**: {audience}", ""])

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


def convert_markdown(
    md_path: Path,
    html_path: Path,
    title: str,
    template: Path,
    *,
    quadrant: str | None = None,
    cssroot: str = "",
) -> None:
    """Convert a single markdown file to HTML via pandoc."""
    html_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pandoc", str(md_path),
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
    if result.returncode != 0:
        print(f"  pandoc error for {md_path}: {result.stderr}", file=sys.stderr)
    else:
        # Fix 2: Pandoc preserves .md extensions in href attributes — convert to .html
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


def insert_exercise_iframes(html_path: Path, exercises: list[str]) -> None:
    """Append exercise iframes to an HTML file."""
    if not exercises:
        return

    iframe_blocks = []
    for ex in exercises:
        stem = Path(ex).stem
        iframe_blocks.append(textwrap.dedent(f"""\
            <div class="marimo-exercise">
                <h3>Exercise: {stem.replace('-', ' ').replace('_', ' ').title()}</h3>
                <iframe
                    src="http://localhost:{MARIMO_PORT}/{stem}"
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


def build(diataxis_dir: Path) -> None:
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
        convert_markdown(home_md, home_html, structure.get("project", {}).get("name", "Home"), template)
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
                md_file, html_path, title, template,
                quadrant=quadrant,
                cssroot=cssroot,
            )

            # Inject sidebar with correct relative paths
            current_href = f"{quadrant}/{html_rel.name}"
            inject_sidebar(html_path, sidebar_html, current_href)

            # Insert exercise iframes if applicable
            rel_str = str(rel)
            if rel_str in file_exercises:
                insert_exercise_iframes(html_path, file_exercises[rel_str])

    # Generate marimo ASGI config if there are exercises
    if exercise_map:
        generate_marimo_config(diataxis_dir, exercise_map)

    print(f"Build complete: {build_dir}")


# ---------------------------------------------------------------------------
# Marimo server config generation
# ---------------------------------------------------------------------------


def generate_marimo_config(diataxis_dir: Path, exercise_map: dict[str, str]) -> None:
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
        "    import uvicorn",
        f'    uvicorn.run(app, host="localhost", port={MARIMO_PORT})',
        "",
    ])

    config_path = diataxis_dir / "_serve_exercises.py"
    config_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated marimo config: {config_path}")


# ---------------------------------------------------------------------------
# Serve
# ---------------------------------------------------------------------------


def serve(diataxis_dir: Path) -> None:
    """Start both static and marimo servers."""
    build_dir = diataxis_dir / "_build"
    if not build_dir.exists():
        print("Build directory not found. Run build first.", file=sys.stderr)
        sys.exit(1)

    exercise_script = diataxis_dir / "_serve_exercises.py"

    # Start marimo server if exercises exist
    # Use uv run so packages installed by uv are available
    marimo_proc = None
    if exercise_script.exists():
        print(f"Starting marimo server on port {MARIMO_PORT}...")
        marimo_proc = subprocess.Popen(
            ["uv", "run", "python", str(exercise_script)],
            cwd=str(diataxis_dir),
        )

    # Start static server
    print(f"Starting static server on port {STATIC_PORT}...")
    print(f"Open http://localhost:{STATIC_PORT} in your browser.")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir), **kwargs)

    try:
        server = http.server.HTTPServer(("localhost", STATIC_PORT), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if marimo_proc is not None:
            marimo_proc.terminate()
            marimo_proc.wait()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Diataxis documentation build pipeline")
    parser.add_argument(
        "diataxis_dir",
        nargs="?",
        default="diataxis",
        help="Path to the diataxis directory (default: ./diataxis)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start servers after building",
    )
    parser.add_argument(
        "--serve-only",
        action="store_true",
        help="Start servers without rebuilding",
    )
    args = parser.parse_args()

    diataxis_dir = Path(args.diataxis_dir).resolve()

    if not args.serve_only:
        build(diataxis_dir)

    if args.serve or args.serve_only:
        serve(diataxis_dir)


if __name__ == "__main__":
    main()
