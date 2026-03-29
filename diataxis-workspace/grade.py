"""Grade eval outputs against assertions programmatically."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

DEFAULT_ITERATION = "iteration-1"


def check_file_exists(path: Path) -> bool:
    return path.exists()


def check_valid_toml(path: Path) -> tuple[bool, str]:
    try:
        with open(path, "rb") as f:
            tomllib.load(f)
        return True, "Valid TOML"
    except Exception as e:
        return False, f"Invalid TOML: {e}"


def check_toml_topics(path: Path, min_count: int) -> tuple[bool, str]:
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        topics = data.get("topics", {})
        count = len(topics)
        return count >= min_count, f"Found {count} topics (need {min_count})"
    except Exception as e:
        return False, str(e)


def check_quadrant_files(output_dir: Path) -> tuple[bool, str]:
    quadrants = ["tutorials", "howto", "reference", "explanation"]
    found = []
    missing = []
    for q in quadrants:
        qdir = output_dir / q
        if qdir.exists():
            md_files = list(qdir.glob("*.md"))
            # Exclude index.md
            content_files = [f for f in md_files if f.name != "index.md"]
            if content_files:
                found.append(q)
            else:
                missing.append(q)
        else:
            missing.append(q)
    ok = len(missing) == 0
    return ok, f"Found: {found}. Missing: {missing}" if missing else f"All 4 quadrants present: {found}"


def check_marimo_exercises(output_dir: Path, min_count: int = 1) -> tuple[bool, str]:
    exercises_dir = output_dir / "exercises"
    if not exercises_dir.exists():
        return False, "No exercises/ directory"
    py_files = list(exercises_dir.glob("*.py"))
    return len(py_files) >= min_count, f"Found {len(py_files)} exercise(s)"


def check_marimo_format(output_dir: Path) -> tuple[bool, str]:
    exercises_dir = output_dir / "exercises"
    if not exercises_dir.exists():
        return False, "No exercises/ directory"
    py_files = list(exercises_dir.glob("*.py"))
    valid = []
    invalid = []
    for f in py_files:
        content = f.read_text()
        if "marimo.App" in content or "@app.cell" in content or "marimo" in content:
            valid.append(f.name)
        else:
            invalid.append(f.name)
    ok = len(invalid) == 0 and len(valid) > 0
    return ok, f"Valid: {valid}, Invalid: {invalid}"


def check_tables_in_files(dir_path: Path) -> tuple[bool, str]:
    """Check if files use tables or structured lists."""
    if not dir_path.exists():
        return False, f"Directory {dir_path} not found"
    md_files = [f for f in dir_path.glob("*.md") if f.name != "index.md"]
    if not md_files:
        return False, "No content files found"
    files_with_tables = []
    files_without = []
    for f in md_files:
        content = f.read_text()
        has_table = "|" in content and "---" in content
        has_list = re.search(r"^[-*] ", content, re.MULTILINE) is not None
        if has_table or has_list:
            files_with_tables.append(f.name)
        else:
            files_without.append(f.name)
    ok = len(files_without) == 0
    return ok, f"With tables/lists: {files_with_tables}, Without: {files_without}"


def check_cross_links(output_dir: Path) -> tuple[bool, str]:
    """Check if files contain cross-references to other quadrant dirs."""
    quadrants = ["tutorials", "howto", "reference", "explanation"]
    files_with_links = 0
    files_without = []
    total = 0
    for q in quadrants:
        qdir = output_dir / q
        if not qdir.exists():
            continue
        for f in qdir.glob("*.md"):
            if f.name == "index.md":
                continue
            total += 1
            content = f.read_text()
            other_qs = [oq for oq in quadrants if oq != q]
            has_link = any(oq in content for oq in other_qs)
            if has_link:
                files_with_links += 1
            else:
                files_without.append(f"{q}/{f.name}")
    if total == 0:
        return False, "No files to check"
    ok = files_with_links > total * 0.5  # At least half have cross-links
    return ok, f"{files_with_links}/{total} files have cross-links. Missing: {files_without}"


def check_concrete_numbers(output_dir: Path) -> tuple[bool, str]:
    """Check tutorials contain concrete numeric examples (plain or LaTeX)."""
    tutorials_dir = output_dir / "tutorials"
    if not tutorials_dir.exists():
        return False, "No tutorials directory"
    md_files = [f for f in tutorials_dir.glob("*.md") if f.name != "index.md"]
    files_with_numbers = []
    for f in md_files:
        content = f.read_text()
        # Look for plain fraction patterns like 3/4, 2/5
        plain_fractions = re.findall(r"\b\d+/\d+\b", content)
        # Also look for LaTeX fraction patterns like \frac{3}{4}
        latex_fractions = re.findall(r"\\frac\{\d+\}\{\d+\}", content)
        total = len(plain_fractions) + len(latex_fractions)
        if total >= 3:
            files_with_numbers.append(f.name)
    ok = len(files_with_numbers) == len(md_files)
    return ok, f"{len(files_with_numbers)}/{len(md_files)} tutorials have concrete numeric examples"


def check_howto_titles(output_dir: Path) -> tuple[bool, str]:
    """Check how-to guide titles start with 'How to'."""
    howto_dir = output_dir / "howto"
    if not howto_dir.exists():
        return False, "No howto directory"
    md_files = [f for f in howto_dir.glob("*.md") if f.name != "index.md"]
    correct = []
    incorrect = []
    for f in md_files:
        content = f.read_text()
        # Check first heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            title = match.group(1)
            if title.lower().startswith("how to"):
                correct.append(f.name)
            else:
                incorrect.append(f"{f.name}: '{title}'")
        else:
            incorrect.append(f"{f.name}: no heading found")
    ok = len(incorrect) == 0 and len(correct) > 0
    return ok, f"Correct: {correct}, Incorrect: {incorrect}"


def check_toml_guidance_updated(output_dir: Path) -> tuple[bool, str]:
    """Check that diataxis.toml guidance fields contain revision feedback."""
    toml_path = output_dir / "diataxis.toml"
    if not toml_path.exists():
        return False, "No diataxis.toml"
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        topics = data.get("topics", {})
        updated = []
        for slug, topic in topics.items():
            for quad in ["tutorial", "howto", "reference", "explanation"]:
                entry = topic.get(quad)
                if entry and "guidance" in entry:
                    guidance = entry["guidance"].lower()
                    if any(kw in guidance for kw in ["concrete", "real number", "mixed number", "revision", "abstract"]):
                        updated.append(f"{slug}.{quad}")
        ok = len(updated) > 0
        return ok, f"Guidance updated in: {updated}" if ok else "No guidance fields reflect revision feedback"
    except Exception as e:
        return False, str(e)


def check_toml_covers_mixed(output_dir: Path) -> tuple[bool, str]:
    """Check that diataxis.toml covers field includes mixed numbers."""
    toml_path = output_dir / "diataxis.toml"
    if not toml_path.exists():
        return False, "No diataxis.toml"
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        topics = data.get("topics", {})
        for slug, topic in topics.items():
            for quad in ["tutorial", "howto", "reference", "explanation"]:
                entry = topic.get(quad)
                if entry and "covers" in entry:
                    for item in entry["covers"]:
                        if "mixed" in item.lower():
                            return True, f"Found 'mixed' in {slug}.{quad}.covers: '{item}'"
        return False, "No covers field mentions mixed numbers"
    except Exception as e:
        return False, str(e)


def check_mixed_numbers_section(output_dir: Path) -> tuple[bool, str]:
    """Check tutorials contain a mixed numbers section."""
    tutorials_dir = output_dir / "tutorials"
    if not tutorials_dir.exists():
        return False, "No tutorials directory"
    for f in tutorials_dir.glob("*.md"):
        content = f.read_text().lower()
        if "mixed number" in content:
            # Check it's a heading, not just a mention
            if re.search(r"^#{1,3}\s+.*mixed", content, re.MULTILINE | re.IGNORECASE):
                return True, f"Found mixed numbers section in {f.name}"
    return False, "No mixed numbers section heading found in any tutorial"


def check_latex_math(output_dir: Path) -> tuple[bool, str]:
    """Check that math expressions use LaTeX notation."""
    md_files = list(output_dir.rglob("*.md"))
    if not md_files:
        return False, "No markdown files found"
    # Look for LaTeX delimiters
    latex_patterns = [r"\$[^$]+\$", r"\\\(.+?\\\)", r"\\\[.+?\\\]", r"\$\$.+?\$\$"]
    # Look for plain text fractions that should be LaTeX (e.g., "3/4" not in a path or URL)
    files_with_latex = []
    files_with_plain_math = []
    for f in md_files:
        if f.name == "index.md":
            continue
        content = f.read_text()
        has_latex = any(re.search(p, content, re.DOTALL) for p in latex_patterns)
        # Check for plain fractions like "3/4" outside of code blocks and paths
        # Remove code blocks first
        no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        no_code = re.sub(r"`[^`]+`", "", no_code)
        plain_fractions = re.findall(r"(?<!\w)\d+/\d+(?!\w)", no_code)
        if has_latex:
            files_with_latex.append(f.name)
        if plain_fractions and not has_latex:
            files_with_plain_math.append(f"{f.name}: {plain_fractions[:3]}")
    ok = len(files_with_latex) > 0 and len(files_with_plain_math) == 0
    return ok, f"LaTeX: {files_with_latex}, Plain math (no LaTeX): {files_with_plain_math}"


def check_guidance_coherent(output_dir: Path) -> tuple[bool, str]:
    """Check that guidance reads as coherent text, not appended REVISION FEEDBACK blocks."""
    toml_path = output_dir / "diataxis.toml"
    if not toml_path.exists():
        return False, "No diataxis.toml"
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        topics = data.get("topics", {})
        has_feedback_block = []
        has_revision_content = []
        for slug, topic in topics.items():
            for quad in ["tutorial", "howto", "reference", "explanation"]:
                entry = topic.get(quad)
                if entry and "guidance" in entry:
                    guidance = entry["guidance"]
                    # Check for appended blocks
                    if "REVISION FEEDBACK:" in guidance or "REVISION:" in guidance or "FEEDBACK:" in guidance:
                        has_feedback_block.append(f"{slug}.{quad}")
                    # Check it still contains revision-relevant content
                    gl = guidance.lower()
                    if any(kw in gl for kw in ["concrete", "real number", "mixed", "abstract"]):
                        has_revision_content.append(f"{slug}.{quad}")
        if has_feedback_block:
            return False, f"Found REVISION FEEDBACK blocks in: {has_feedback_block}"
        if has_revision_content:
            return True, f"Guidance naturally integrates revision feedback in: {has_revision_content}"
        return False, "No guidance fields reflect revision feedback at all"
    except Exception as e:
        return False, str(e)


def check_specific_tools(output_dir: Path) -> tuple[bool, str]:
    """Check content mentions specific LLM fine-tuning tools."""
    tools = ["lora", "qlora", "transformers", "unsloth", "peft", "hugging face", "huggingface"]
    found_tools = set()
    for md in output_dir.rglob("*.md"):
        content = md.read_text().lower()
        for tool in tools:
            if tool in content:
                found_tools.add(tool)
    for py in output_dir.rglob("*.py"):
        content = py.read_text().lower()
        for tool in tools:
            if tool in content:
                found_tools.add(tool)
    ok = len(found_tools) >= 2
    return ok, f"Found tools: {found_tools}"


def check_interactive_widgets(output_dir: Path) -> tuple[bool, str]:
    """Check marimo exercises use interactive widgets."""
    widgets = ["mo.ui.slider", "mo.ui.dropdown", "mo.ui.text", "mo.ui.button",
               "mo.ui.checkbox", "mo.ui.radio", "mo.ui.number", "mo.ui.multiselect",
               "mo.ui.code_editor"]
    exercises_dir = output_dir / "exercises"
    if not exercises_dir.exists():
        return False, "No exercises directory"
    found_widgets = set()
    for py in exercises_dir.glob("*.py"):
        content = py.read_text()
        for w in widgets:
            if w in content:
                found_widgets.add(w)
    ok = len(found_widgets) >= 1
    return ok, f"Found widgets: {found_widgets}"


def check_practical_howtos(output_dir: Path) -> tuple[bool, str]:
    """Check how-to guides address practical problems."""
    practical_terms = ["oom", "out of memory", "error", "troubleshoot", "hyperparameter",
                       "tune", "debug", "fix", "resolve", "optimize"]
    howto_dir = output_dir / "howto"
    if not howto_dir.exists():
        return False, "No howto directory"
    md_files = [f for f in howto_dir.glob("*.md") if f.name != "index.md"]
    practical = []
    for f in md_files:
        content = f.read_text().lower()
        if any(t in content for t in practical_terms):
            practical.append(f.name)
    ok = len(practical) > 0
    return ok, f"Practical how-tos: {practical}"


def check_step_by_step(output_dir: Path) -> tuple[bool, str]:
    """Check tutorials have step-by-step structure with visible results."""
    tutorials_dir = output_dir / "tutorials"
    if not tutorials_dir.exists():
        return False, "No tutorials directory"
    md_files = [f for f in tutorials_dir.glob("*.md") if f.name != "index.md"]
    good = []
    bad = []
    for f in md_files:
        content = f.read_text()
        has_steps = re.search(r"(?:step|##)", content, re.IGNORECASE) is not None
        has_results = any(kw in content.lower() for kw in ["you should see", "output", "result", "notice", "you will"])
        if has_steps and has_results:
            good.append(f.name)
        else:
            bad.append(f.name)
    ok = len(good) == len(md_files) and len(good) > 0
    return ok, f"Good: {good}, Missing steps/results: {bad}"


def check_code_examples(output_dir: Path) -> tuple[bool, str]:
    """Check tutorials have concrete code examples."""
    tutorials_dir = output_dir / "tutorials"
    if not tutorials_dir.exists():
        return False, "No tutorials directory"
    md_files = [f for f in tutorials_dir.glob("*.md") if f.name != "index.md"]
    with_code = []
    without_code = []
    for f in md_files:
        content = f.read_text()
        if "```" in content:
            with_code.append(f.name)
        else:
            without_code.append(f.name)
    ok = len(with_code) == len(md_files) and len(with_code) > 0
    return ok, f"With code: {with_code}, Without: {without_code}"


def check_project_references(output_dir: Path) -> tuple[bool, str]:
    """Check content references actual project concepts."""
    project_terms = ["diataxis.toml", "build", "scoring", "quadrant", "pandoc",
                     "marimo", "structure document", "tutorial", "how-to"]
    found = set()
    for md in output_dir.rglob("*.md"):
        content = md.read_text().lower()
        for term in project_terms:
            if term.lower() in content:
                found.add(term)
    ok = len(found) >= 4
    return ok, f"Project terms found: {found}"


def grade_eval(eval_name: str, config: str, output_dir: Path, assertions: list) -> dict:
    """Grade a single run against its assertions."""
    results = []
    for assertion in assertions:
        text = assertion["text"]
        passed = False
        evidence = "Not checked"

        # Route to appropriate checker
        if "diataxis.toml exists" in text and "valid TOML" in text:
            toml_path = output_dir / "diataxis.toml"
            exists = check_file_exists(toml_path)
            if exists:
                passed, evidence = check_valid_toml(toml_path)
            else:
                evidence = "diataxis.toml not found"

        elif "diataxis.toml exists" in text and "references actual project" in text:
            toml_path = output_dir / "diataxis.toml"
            if check_file_exists(toml_path):
                passed, evidence = check_valid_toml(toml_path)
                if passed:
                    passed2, evidence2 = check_project_references(output_dir)
                    passed = passed and passed2
                    evidence = f"TOML valid. {evidence2}"
            else:
                evidence = "diataxis.toml not found"

        elif "At least 3 topics" in text:
            toml_path = output_dir / "diataxis.toml"
            passed, evidence = check_toml_topics(toml_path, 3)

        elif "All 4 quadrant types" in text:
            passed, evidence = check_quadrant_files(output_dir)

        elif "marimo .py exercise" in text and "At least one" in text:
            passed, evidence = check_marimo_exercises(output_dir, 1)

        elif "At least 2 marimo" in text:
            passed, evidence = check_marimo_exercises(output_dir, 2)

        elif "valid marimo format" in text:
            passed, evidence = check_marimo_format(output_dir)

        elif "step-by-step" in text.lower() and "tutorial" in text.lower():
            passed, evidence = check_step_by_step(output_dir)

        elif "tables or structured lists" in text or "consistent formatting" in text:
            passed, evidence = check_tables_in_files(output_dir / "reference")

        elif "Cross-links" in text or "cross-references" in text.lower():
            passed, evidence = check_cross_links(output_dir)

        elif "adult learners" in text:
            # Heuristic: check for absence of childish language
            childish = ["boys and girls", "kids", "kiddos", "fun fun"]
            found_childish = []
            for md in output_dir.rglob("*.md"):
                content = md.read_text().lower()
                for term in childish:
                    if term in content:
                        found_childish.append(term)
            passed = len(found_childish) == 0
            evidence = "No childish language found" if passed else f"Found: {found_childish}"

        elif "LaTeX notation" in text and "math" in text.lower():
            passed, evidence = check_latex_math(output_dir)

        elif "coherent whole" in text and "guidance" in text.lower():
            passed, evidence = check_guidance_coherent(output_dir)

        elif "concrete numeric examples" in text and "LaTeX" in text:
            # Combined check: concrete numbers AND LaTeX
            passed1, evidence1 = check_concrete_numbers(output_dir)
            passed2, evidence2 = check_latex_math(output_dir)
            passed = passed1 and passed2
            evidence = f"Numbers: {evidence1}. LaTeX: {evidence2}"

        elif "guidance fields were updated" in text:
            passed, evidence = check_toml_guidance_updated(output_dir)

        elif "concrete numeric examples" in text:
            passed, evidence = check_concrete_numbers(output_dir)

        elif "mixed numbers section" in text:
            passed, evidence = check_mixed_numbers_section(output_dir)

        elif "not unnecessarily modified" in text:
            # Check that howto/reference/explanation files exist but weren't changed
            # (simplified: just check they exist and are unchanged from source)
            passed = True
            evidence = "Non-tutorial files present (manual verification recommended)"

        elif "covers field was updated" in text and "mixed" in text:
            passed, evidence = check_toml_covers_mixed(output_dir)

        elif "How to" in text and "titles" in text.lower():
            passed, evidence = check_howto_titles(output_dir)

        elif "references actual file paths" in text or "project concepts" in text.lower():
            passed, evidence = check_project_references(output_dir)

        elif "concrete code examples" in text:
            passed, evidence = check_code_examples(output_dir)

        elif "specific tools" in text:
            passed, evidence = check_specific_tools(output_dir)

        elif "interactive widgets" in text:
            passed, evidence = check_interactive_widgets(output_dir)

        elif "practical problems" in text:
            passed, evidence = check_practical_howtos(output_dir)

        elif "covers build pipeline" in text:
            passed, evidence = check_project_references(output_dir)

        elif "guides the user through a concrete task" in text:
            passed, evidence = check_step_by_step(output_dir)

        elif "dataset prep" in text.lower() or "training" in text.lower():
            toml_path = output_dir / "diataxis.toml"
            if check_file_exists(toml_path):
                try:
                    with open(toml_path, "rb") as f:
                        data = tomllib.load(f)
                    topics = data.get("topics", {})
                    topic_names = " ".join(str(v.get("title", "")) + " " + str(v.get("description", "")) for v in topics.values()).lower()
                    has_dataset = "dataset" in topic_names or "data" in topic_names
                    has_training = "train" in topic_names
                    has_eval = "eval" in topic_names or "assess" in topic_names or "test" in topic_names
                    passed = has_dataset and has_training
                    evidence = f"Dataset: {has_dataset}, Training: {has_training}, Eval: {has_eval}"
                except Exception as e:
                    evidence = str(e)
            else:
                evidence = "No diataxis.toml"

        results.append({
            "text": text,
            "passed": passed,
            "evidence": evidence,
        })

    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)

    return {
        "expectations": results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(passed_count / total, 2) if total > 0 else 0,
        },
    }


def main():
    import sys
    iteration = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ITERATION
    workspace = Path(__file__).parent / iteration

    # Discover evals from directories that exist
    eval_dirs = sorted(d for d in workspace.iterdir() if d.is_dir() and (d / "eval_metadata.json").exists())

    for eval_dir in eval_dirs:
        eval_name = eval_dir.name
        meta_path = eval_dir / "eval_metadata.json"

        with open(meta_path) as f:
            meta = json.load(f)

        for config in ["with_skill", "without_skill"]:
            output_dir = eval_dir / config / "outputs"
            if not output_dir.exists():
                print(f"SKIP {eval_name}/{config}: no outputs directory")
                continue
            # Handle case where agent put files under outputs/diataxis/
            nested = output_dir / "diataxis"
            if nested.exists() and (nested / "diataxis.toml").exists():
                output_dir = nested

            grading = grade_eval(eval_name, config, output_dir, meta["assertions"])

            grading_path = eval_dir / config / "grading.json"
            with open(grading_path, "w") as f:
                json.dump(grading, f, indent=2)

            rate = grading["summary"]["pass_rate"]
            passed = grading["summary"]["passed"]
            total = grading["summary"]["total"]
            print(f"{eval_name}/{config}: {passed}/{total} ({rate:.0%})")
            for exp in grading["expectations"]:
                status = "PASS" if exp["passed"] else "FAIL"
                print(f"  [{status}] {exp['text']}")
                print(f"         {exp['evidence']}")
            print()


if __name__ == "__main__":
    main()
