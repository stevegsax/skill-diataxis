#!/usr/bin/env python3
r"""Upgrade a pre-Hugo diataxis/ directory in place.

Pre-Hugo projects were produced by an earlier build pipeline. They use the
same `diataxis.toml` schema as the current Hugo pipeline, but the markdown
files have no TOML frontmatter, the directory has no `hugo.toml`/`Makefile`/
`go.mod`, there are no `_index.md` quadrant landing pages, and internal
links point at `.html` files instead of Hugo's pretty-URL directories.

This script performs the mechanical part of the migration:

  1. Scaffolds `hugo.toml`, `Makefile`, and `go.mod` from the skill's
     templates (only if missing — existing files are never overwritten).
  2. Adds TOML frontmatter to every quadrant content file listed in
     `diataxis.toml`. Title is taken from the file's first body H1 when
     present, else derived from the filename. Weight is
     `topic.order * 10 + quadrant_weight` (explanation=1, tutorials=2,
     howto=3, reference=4). `topic`, `covers`, and `detail` are copied
     verbatim from the matching `diataxis.toml` entry. `description` is
     the topic's `description` field.
  3. Removes the body H1 line (Hugo themes render the title from
     frontmatter; a body H1 produces a duplicate heading).
  4. Rewrites `.html` and `/index.html` markdown links to Hugo pretty-URL
     directory form.
  5. Adds frontmatter + `[cascade] type = "docs"` to the homepage
     (`index.md`) if it exists and lacks frontmatter.
  6. Renames stray `<quadrant>/index.md` files (a common artifact of
     documentation ported from Jekyll, MkDocs, Docusaurus, and similar
     tools) to `<quadrant>/_index.md`. Hugo treats a directory that
     contains `index.md` as a leaf bundle and silently suppresses the
     section listing — the section page renders `index.md` instead of
     the auto-generated list of child pages. Body content is preserved;
     frontmatter is prepended if missing. If both `index.md` and
     `_index.md` already exist in the same quadrant, the file is left
     alone and surfaced in the report for manual resolution.
  7. Creates `_index.md` for each quadrant directory that is missing one,
     with the canonical section weight (explanation=10, tutorials=20,
     howto=30, reference=40), a short introduction, and a bulleted list
     of links to every content file in that quadrant ordered by weight.
  8. Rewrites math delimiters: `$...$` → `\(...\)` and `$$...$$` →
     `\[...\]`. The dollar-sign form is what the pre-Hugo diataxis
     pipeline and most other static-site generators use; the skill
     canonicalizes on the LaTeX form. Code blocks (fenced and inline)
     are preserved verbatim, and inline dollar spans are only
     converted when the content looks like math so prose mentions of
     currency ("costs $5") are not clobbered.

Idempotent: running on an already-upgraded directory is a no-op. Files
with existing frontmatter are never rewritten. `hugo.toml`, `Makefile`,
and `go.mod` are never overwritten.

What this script does NOT do:
  - Rewrite `guidance` fields in `diataxis.toml` that reference retired
    tools (e.g. `pandoc`, `mmdc`, `uv run diataxis build`). Guidance
    represents the author's intent; an LLM should review it after the
    mechanical upgrade and integrate changes the way the skill's
    revision workflow requires.
  - Restructure exercises or append an `## Exercises` section. Existing
    exercise references are preserved as-is.
  - Migrate `scores.toml`. The schema has not changed.

Usage:
  python upgrade_to_hugo.py <diataxis_dir>          # perform upgrade
  python upgrade_to_hugo.py <diataxis_dir> --check  # detect only, exit 1
                                                     #   if upgrade needed
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tomllib
from pathlib import Path

QUADRANT_WEIGHTS = {
    "explanation": 1,
    "tutorials": 2,
    "howto": 3,
    "reference": 4,
}

SECTION_WEIGHTS = {
    "explanation": 10,
    "tutorials": 20,
    "howto": 30,
    "reference": 40,
}

QUADRANT_LABELS = {
    "explanation": "Explanation",
    "tutorials": "Tutorials",
    "howto": "How-to Guides",
    "reference": "Reference",
}

QUADRANT_INTROS = {
    "explanation": (
        "Explanation documents discuss the why — the reasoning, design "
        "rationale, and trade-offs behind the project. Read these to deepen "
        "understanding, not to accomplish a task."
    ),
    "tutorials": (
        "Tutorials are lessons that take you through a sequence of steps to "
        "produce a concrete result. Read these to start using the project."
    ),
    "howto": (
        "How-to guides are recipes for accomplishing a specific task. Read "
        "these when you already know what you are doing and need to get "
        "something done."
    ),
    "reference": (
        "Reference documents describe the technical machinery — APIs, "
        "configuration, and data shapes. Read these when you need exact "
        "information."
    ),
}

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

RETIRED_TOOL_PATTERNS = [
    r"\bpandoc\b",
    r"\bmmdc\b",
    r"uv run diataxis (build|serve|serve-only|publish)",
    r"diataxis/_build/",
]


def load_structure(diataxis_dir: Path) -> dict:
    toml_path = diataxis_dir / "diataxis.toml"
    if not toml_path.exists():
        raise SystemExit(
            f"diataxis.toml not found at {toml_path}. The upgrade needs a "
            "structure document to map content files to their topic metadata."
        )
    with toml_path.open("rb") as f:
        return tomllib.load(f)


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "project"


def title_from_filename(path: Path) -> str:
    return " ".join(w.capitalize() for w in path.stem.split("-"))


def detect_pre_hugo(diataxis_dir: Path) -> dict:
    """Report pre-Hugo artifacts found under ``diataxis_dir``.

    Returns a dict whose presence of keys indicates what needs migrating.
    Empty dict means the directory is already in Hugo format.
    """
    report: dict = {}

    for filename in ("hugo.toml", "Makefile", "go.mod"):
        if not (diataxis_dir / filename).exists():
            report.setdefault("missing_config", []).append(filename)

    missing_fm: list[str] = []
    for quadrant in QUADRANT_WEIGHTS:
        qdir = diataxis_dir / quadrant
        if not qdir.is_dir():
            continue
        for md in sorted(qdir.glob("*.md")):
            if md.name in ("_index.md", "index.md"):
                continue
            if not md.read_text().startswith("+++"):
                missing_fm.append(str(md.relative_to(diataxis_dir)))
    if missing_fm:
        report["files_without_frontmatter"] = missing_fm

    missing_landing: list[str] = []
    for quadrant in QUADRANT_WEIGHTS:
        qdir = diataxis_dir / quadrant
        if qdir.is_dir() and not (qdir / "_index.md").exists():
            missing_landing.append(f"{quadrant}/_index.md")
    if missing_landing:
        report["missing_quadrant_landing_pages"] = missing_landing

    # `<quadrant>/index.md` is a common artifact of docs ported from tools
    # that use `index.md` as a section landing page (Jekyll, MkDocs,
    # Docusaurus, pre-Hugo versions of this skill with hand-written
    # landing pages). Hugo treats any directory containing `index.md` as
    # a leaf bundle and hides the section listing, so these files have to
    # move to `_index.md` before the site renders correctly.
    stray_quadrant_index: list[str] = []
    for quadrant in QUADRANT_WEIGHTS:
        qdir = diataxis_dir / quadrant
        if qdir.is_dir() and (qdir / "index.md").exists():
            stray_quadrant_index.append(f"{quadrant}/index.md")
    if stray_quadrant_index:
        report["stray_quadrant_index_files"] = stray_quadrant_index

    index_md = diataxis_dir / "index.md"
    if index_md.exists() and not index_md.read_text().startswith("+++"):
        report["homepage_without_frontmatter"] = "index.md"

    # Files that use `$...$` / `$$...$$` for math — the inheritance from
    # TeX that most non-Hugo static-site generators share. The skill's
    # canonical form is `\(...\)` / `\[...\]`, and the upgrade rewrites
    # these in place.
    dollar_math: list[str] = []
    candidates = [index_md] if index_md.exists() else []
    for quadrant in QUADRANT_WEIGHTS:
        qdir = diataxis_dir / quadrant
        if qdir.is_dir():
            candidates.extend(sorted(qdir.glob("*.md")))
    for md in candidates:
        try:
            if _has_dollar_math(md.read_text()):
                dollar_math.append(str(md.relative_to(diataxis_dir)))
        except OSError:
            continue
    if dollar_math:
        report["dollar_delimited_math"] = dollar_math

    return report


def extract_h1(text: str) -> tuple[str | None, str]:
    """Split the first H1 off the top of ``text``.

    Walks the leading blank/blank-like lines, then grabs a ``# Title`` line
    if present. Returns ``(title, rest)`` where ``rest`` is the remainder
    with the H1 and trailing blank lines stripped.
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or not lines[i].startswith("# "):
        return None, text
    title = lines[i][2:].strip()
    j = i + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    rest = "\n".join(lines[j:])
    return title, rest


def toml_str(s: str) -> str:
    """Quote ``s`` as a TOML basic string."""
    # Escape backslashes, double quotes, and control chars that break basic
    # strings. Newlines inside a single-line frontmatter value are rare but
    # must be escaped to keep the file parseable.
    escaped = (
        s.replace("\\", "\\\\")
        .replace("\"", "\\\"")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def toml_array(items: list[str]) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(toml_str(s) for s in items) + "]"


def build_file_index(structure: dict) -> dict[str, tuple[str, dict, str, dict]]:
    """Map ``file`` path → ``(topic_slug, topic, quadrant, entry)``."""
    index: dict[str, tuple[str, dict, str, dict]] = {}
    for slug, topic in (structure.get("topics") or {}).items():
        for quadrant in QUADRANT_WEIGHTS:
            entry = topic.get(quadrant)
            if entry and "file" in entry:
                index[entry["file"]] = (slug, topic, quadrant, entry)
    return index


_HTML_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")

# Math-delimiter rewriting. Pre-Hugo diataxis projects — and most static
# site generators outside Hugo (Jekyll, MkDocs, Docusaurus, GitBook) —
# use `$...$` / `$$...$$` for math, inherited from TeX. The skill
# canonicalizes on LaTeX's `\(...\)` / `\[...\]` form, which does not
# collide with literal dollar signs in prose and is less sensitive to
# downstream-tooling quirks.
_FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
# Inline math: `$...$` with no adjacent `$` (which would be display math)
# and no leading backslash (`\$` is an escaped dollar, not math).
_INLINE_MATH_RE = re.compile(r"(?<![\$\\])\$(?!\$)([^\$\n]+?)(?<![\$\\])\$(?!\$)")


def _looks_like_math(span: str) -> bool:
    """Heuristic: does the span between `$` delimiters look like LaTeX?

    Inline dollar rewriting has to avoid false-converting prose that
    mentions currency — `"costs $5 and $10"` must stay intact. A real
    math span almost always contains one of: a LaTeX command
    (backslash), a sub/superscript/brace marker, a relation operator
    (`=`, `<`, `>`), or a short symbolic expression. Prose dollars
    don't.
    """
    if "\\" in span:
        return True
    if re.search(r"[\^_{}=<>]", span):
        return True
    # Lone variable or short symbol: `x`, `n`, `E_0`, `x_1`
    if re.fullmatch(r"\s*[a-zA-Z][a-zA-Z\d]{0,4}\s*", span):
        return True
    # Expression with math operators and alphanumerics
    if re.search(r"[+\-*/]", span) and re.search(r"\w", span):
        return True
    return False


def rewrite_math_delimiters(body: str) -> str:
    """Convert `$...$` → `\\(...\\)` and `$$...$$` → `\\[...\\]`.

    Fenced code blocks and inline code are preserved verbatim — a
    tutorial whose examples show the `$` character must not have its
    markup rewritten. Inline `$...$` conversion is gated on a "looks
    like math" heuristic so prose that happens to mention dollar
    amounts is not clobbered.
    """
    protected: list[str] = []

    def stash(match: re.Match) -> str:
        protected.append(match.group(0))
        return f"\x00STASH{len(protected) - 1}\x00"

    working = _FENCED_CODE_RE.sub(stash, body)
    working = _INLINE_CODE_RE.sub(stash, working)

    # Display math first — $$...$$ is unambiguous and may span multiple
    # lines, so let it consume those spans before inline math sees them.
    working = _DISPLAY_MATH_RE.sub(
        lambda m: f"\\[{m.group(1)}\\]", working
    )

    def replace_inline(m: re.Match) -> str:
        content = m.group(1)
        if _looks_like_math(content):
            return f"\\({content}\\)"
        return m.group(0)

    working = _INLINE_MATH_RE.sub(replace_inline, working)

    for i, snippet in enumerate(protected):
        working = working.replace(f"\x00STASH{i}\x00", snippet)

    return working


def _has_dollar_math(text: str) -> bool:
    """True if `text` contains dollar-delimited math outside code spans."""
    protected = _FENCED_CODE_RE.sub("", text)
    protected = _INLINE_CODE_RE.sub("", protected)
    if _DISPLAY_MATH_RE.search(protected):
        return True
    for m in _INLINE_MATH_RE.finditer(protected):
        if _looks_like_math(m.group(1)):
            return True
    return False


def rewrite_html_links(body: str) -> str:
    """Rewrite Markdown link targets that point at ``.html`` files.

    ``foo/index.html`` → ``foo/`` (directory form) and ``foo/bar.html`` →
    ``foo/bar/``. Leaves external links (``http(s)://``), fragments, and
    mailto URLs alone.
    """

    def repl(match: re.Match) -> str:
        text, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#", "/")):
            return match.group(0)
        # Split fragment/query so the trailing slash lands on the path.
        fragment = ""
        for marker in ("#", "?"):
            if marker in url:
                path_part, _, rest = url.partition(marker)
                fragment = marker + rest
                url = path_part
                break
        if url.endswith("/index.html"):
            new_url = url[: -len("index.html")]
        elif url.endswith(".html"):
            new_url = url[: -len(".html")] + "/"
        else:
            return match.group(0)
        return f"[{text}]({new_url}{fragment})"

    return _HTML_LINK_RE.sub(repl, body)


def build_frontmatter(
    *,
    title: str,
    weight: int,
    description: str,
    topic_slug: str,
    covers: list[str],
    detail: str,
) -> str:
    lines = [
        "+++",
        f"title = {toml_str(title)}",
        f"weight = {weight}",
        f"description = {toml_str(description)}",
        f"topic = {toml_str(topic_slug)}",
        f"covers = {toml_array(covers)}",
        f"detail = {toml_str(detail)}",
        "+++",
    ]
    return "\n".join(lines) + "\n"


def upgrade_content_file(
    md_path: Path,
    topic_slug: str,
    topic: dict,
    quadrant: str,
    entry: dict,
) -> bool:
    text = md_path.read_text()
    if text.startswith("+++"):
        return False

    title, body = extract_h1(text)
    if title is None:
        title = title_from_filename(md_path)

    topic_order = topic.get("order") or 0
    weight = topic_order * 10 + QUADRANT_WEIGHTS[quadrant]

    description = topic.get("description") or ""
    covers = entry.get("covers") or []
    detail = entry.get("detail") or ""

    body = rewrite_html_links(body)
    body = rewrite_math_delimiters(body)

    frontmatter = build_frontmatter(
        title=title,
        weight=weight,
        description=description,
        topic_slug=topic_slug,
        covers=covers,
        detail=detail,
    )
    md_path.write_text(frontmatter + body.lstrip("\n"))
    return True


def upgrade_homepage(diataxis_dir: Path, structure: dict) -> bool:
    index_md = diataxis_dir / "index.md"
    if not index_md.exists():
        return False
    text = index_md.read_text()
    if text.startswith("+++"):
        return False

    title, body = extract_h1(text)
    project = structure.get("project") or {}
    if title is None:
        title = project.get("name") or "Documentation"
    description = project.get("description") or ""

    body = rewrite_html_links(body)
    body = rewrite_math_delimiters(body)

    fm_lines = [
        "+++",
        f"title = {toml_str(title)}",
        f"description = {toml_str(description)}",
        "[cascade]",
        'type = "docs"',
        "+++",
    ]
    frontmatter = "\n".join(fm_lines) + "\n"
    index_md.write_text(frontmatter + body.lstrip("\n"))
    return True


def read_title(md_path: Path) -> str:
    """Read a file's title — from frontmatter if present, else filename."""
    if not md_path.exists():
        return title_from_filename(md_path)
    text = md_path.read_text()
    if text.startswith("+++"):
        match = re.search(r"^title\s*=\s*\"([^\"]*)\"", text, re.MULTILINE)
        if match:
            return match.group(1)
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return title_from_filename(md_path)


def promote_stray_quadrant_index(diataxis_dir: Path, quadrant: str) -> str | None:
    """Rename ``<quadrant>/index.md`` to ``<quadrant>/_index.md``.

    Hugo distinguishes *leaf bundles* from *branch bundles* by the name of
    the landing page: ``index.md`` makes the directory a leaf bundle (a
    single page with attachments), while ``_index.md`` makes it a branch
    bundle (a section page that lists its children). A section directory
    that contains ``index.md`` will serve that page and never list the
    child pages underneath, so a migrated ``tutorials/index.md`` from
    another tool silently breaks the section. This function preserves the
    user's content — body, any existing frontmatter — and just fixes the
    name. If frontmatter is missing, canonical section frontmatter is
    prepended using the first body H1 as the title when present.

    Returns a short status message describing the outcome, or ``None`` if
    there is no ``index.md`` in this quadrant.
    """
    qdir = diataxis_dir / quadrant
    if not qdir.is_dir():
        return None
    stray = qdir / "index.md"
    if not stray.exists():
        return None
    target = qdir / "_index.md"
    if target.exists():
        # Two landing pages would compete. Refuse to guess which the user
        # wants — surface it instead and let a human pick one.
        return (
            f"{quadrant}/index.md and {quadrant}/_index.md both exist — "
            "delete the one you don't want before re-running the upgrade"
        )

    text = stray.read_text()
    if text.startswith("+++"):
        stray.rename(target)
        return f"renamed {quadrant}/index.md to _index.md"

    title, body = extract_h1(text)
    if title is None:
        title = QUADRANT_LABELS[quadrant]
    body = rewrite_html_links(body)
    body = rewrite_math_delimiters(body)

    fm_lines = [
        "+++",
        f"title = {toml_str(title)}",
        f"weight = {SECTION_WEIGHTS[quadrant]}",
        f"description = {toml_str(f'{QUADRANT_LABELS[quadrant]} — section landing page.')}",
        "+++",
    ]
    frontmatter = "\n".join(fm_lines) + "\n"
    target.write_text(frontmatter + body.lstrip("\n"))
    stray.unlink()
    return f"renamed {quadrant}/index.md to _index.md (added frontmatter)"


def ensure_quadrant_landing(diataxis_dir: Path, structure: dict, quadrant: str) -> bool:
    qdir = diataxis_dir / quadrant
    if not qdir.is_dir():
        return False
    index_path = qdir / "_index.md"
    if index_path.exists():
        existing = index_path.read_text()
        if existing.startswith("+++"):
            return False

    entries = []
    for topic in (structure.get("topics") or {}).values():
        entry = topic.get(quadrant)
        if not entry or "file" not in entry:
            continue
        rel = Path(entry["file"])
        if rel.parent.name != quadrant:
            continue
        order = topic.get("order") or 0
        weight = order * 10 + QUADRANT_WEIGHTS[quadrant]
        target = diataxis_dir / rel
        entries.append((weight, rel.stem, read_title(target)))

    entries.sort()

    lines = [
        "+++",
        f'title = "{QUADRANT_LABELS[quadrant]}"',
        f"weight = {SECTION_WEIGHTS[quadrant]}",
        f'description = "{QUADRANT_LABELS[quadrant]} — section landing page."',
        "+++",
        QUADRANT_INTROS[quadrant],
        "",
    ]
    if not entries:
        lines.append("_No content files yet._")
    else:
        for _, stem, link_title in entries:
            lines.append(f"- [{link_title}]({stem}/)")
    lines.append("")

    index_path.write_text("\n".join(lines))
    return True


def scaffold_config(diataxis_dir: Path, structure: dict) -> list[str]:
    project = structure.get("project") or {}
    name = project.get("name") or diataxis_dir.name
    description = project.get("description") or ""
    slug = slugify(name)

    created: list[str] = []

    hugo_toml = diataxis_dir / "hugo.toml"
    if not hugo_toml.exists():
        tmpl = (TEMPLATE_DIR / "hugo.toml").read_text()
        hugo_toml.write_text(
            tmpl.replace("{{PROJECT_NAME}}", name).replace(
                "{{PROJECT_DESCRIPTION}}", description
            )
        )
        created.append("hugo.toml")

    mk = diataxis_dir / "Makefile"
    if not mk.exists():
        shutil.copy(TEMPLATE_DIR / "Makefile", mk)
        created.append("Makefile")

    gm = diataxis_dir / "go.mod"
    if not gm.exists():
        tmpl = (TEMPLATE_DIR / "go.mod").read_text()
        gm.write_text(tmpl.replace("{{MODULE_PATH}}", f"diataxis.local/{slug}"))
        created.append("go.mod")

    return created


def find_retired_tool_refs(structure: dict) -> list[dict]:
    """Find `diataxis.toml` guidance that mentions retired tools.

    These are not rewritten — guidance encodes the author's intent, so the
    caller (the skill or the user) decides what to do with them. The
    upgrade script just surfaces them.
    """
    flags: list[dict] = []
    patterns = [re.compile(p) for p in RETIRED_TOOL_PATTERNS]
    for slug, topic in (structure.get("topics") or {}).items():
        for quadrant in QUADRANT_WEIGHTS:
            entry = topic.get(quadrant)
            if not entry:
                continue
            for field in ("covers", "detail", "guidance"):
                value = entry.get(field)
                if value is None:
                    continue
                text = " ".join(value) if isinstance(value, list) else str(value)
                for pat in patterns:
                    if pat.search(text):
                        flags.append(
                            {
                                "topic": slug,
                                "quadrant": quadrant,
                                "field": field,
                                "pattern": pat.pattern,
                            }
                        )
                        break
    return flags


def run_upgrade(diataxis_dir: Path) -> dict:
    structure = load_structure(diataxis_dir)
    changes: list[str] = []

    for name in scaffold_config(diataxis_dir, structure):
        changes.append(f"scaffolded {name}")

    if upgrade_homepage(diataxis_dir, structure):
        changes.append("upgraded index.md")

    for rel_path, (topic_slug, topic, quadrant, entry) in build_file_index(structure).items():
        md = diataxis_dir / rel_path
        if md.exists() and upgrade_content_file(md, topic_slug, topic, quadrant, entry):
            changes.append(f"upgraded {rel_path}")

    # Promote stray `index.md` files before creating missing landing pages
    # so the new `_index.md` does not collide with a file we are about to
    # rename into place.
    for quadrant in QUADRANT_WEIGHTS:
        msg = promote_stray_quadrant_index(diataxis_dir, quadrant)
        if msg is not None:
            changes.append(msg)

    for quadrant in QUADRANT_WEIGHTS:
        if ensure_quadrant_landing(diataxis_dir, structure, quadrant):
            changes.append(f"created {quadrant}/_index.md")

    return {
        "changes": changes,
        "retired_tool_refs": find_retired_tool_refs(structure),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Upgrade a pre-Hugo diataxis/ directory in place."
    )
    ap.add_argument("diataxis_dir", help="Path to the diataxis/ directory to upgrade")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Detect only. Exit 1 if upgrade is needed, 0 if already in Hugo format.",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit the detection or upgrade report as JSON.",
    )
    args = ap.parse_args()

    dd = Path(args.diataxis_dir).resolve()
    if not dd.is_dir():
        print(f"error: {dd} is not a directory", file=sys.stderr)
        return 2

    detected = detect_pre_hugo(dd)

    if args.check:
        if args.json:
            print(json.dumps({"diataxis_dir": str(dd), "detected": detected}, indent=2))
        else:
            if not detected:
                print(f"{dd} is already in Hugo format.")
            else:
                print(f"Pre-Hugo artifacts detected in {dd}:")
                for key, value in detected.items():
                    if isinstance(value, list):
                        print(f"  - {key} ({len(value)}):")
                        for item in value:
                            print(f"      {item}")
                    else:
                        print(f"  - {key}: {value}")
        return 1 if detected else 0

    if not detected:
        msg = f"{dd} is already in Hugo format. No upgrade needed."
        if args.json:
            print(json.dumps({"diataxis_dir": str(dd), "changes": [], "retired_tool_refs": []}, indent=2))
        else:
            print(msg)
        return 0

    report = run_upgrade(dd)
    if args.json:
        print(json.dumps({"diataxis_dir": str(dd), **report}, indent=2))
        return 0

    print(f"Upgraded {dd}:")
    for change in report["changes"]:
        print(f"  - {change}")
    if report["retired_tool_refs"]:
        print()
        print("Guidance fields reference retired tools (review manually):")
        for flag in report["retired_tool_refs"]:
            print(
                f"  - topic '{flag['topic']}' / {flag['quadrant']}.{flag['field']} "
                f"matches /{flag['pattern']}/"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
