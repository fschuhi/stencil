#!/usr/bin/env python3
"""Render each project's generated artefacts (e.g. LLM_INSTRUCTIONS.md) from
data/templates.yaml + data/projects.yaml.

Usage:
    python scripts/render.py                # render every project
    python scripts/render.py --project NAME  # render only one project
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import jinja2
import yaml

PROJECTS_YAML = Path("data/projects.yaml")
TEMPLATES_YAML = Path("data/templates.yaml")


def render_project(name: str, tags: list[str], template_str: str) -> str:
    """Pure rendering step: name and tags in, rendered text out. No file I/O here."""
    template = jinja2.Environment().from_string(template_str)
    return template.render(name=name, tags=tags)


def split_at_boundary(text: str, boundary: str = "---") -> str:
    """Return everything after the first standalone boundary line.

    A standalone boundary line is a line whose stripped content equals
    `boundary` exactly -- a line merely containing it (e.g. a Markdown
    table separator like "| --- | --- |") does not match. The boundary
    line itself is discarded; the returned body is otherwise byte-for-byte
    what followed it, with no stripping or re-indenting.

    Raises ValueError if no standalone boundary line is found.
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() == boundary:
            return "".join(lines[i + 1:])
    raise ValueError(f"No standalone {boundary!r} line found")


def load_projects(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_templates(path: Path) -> list:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def select_projects(projects: dict, project_name: str | None) -> dict:
    if project_name is None:
        return projects
    if project_name not in projects:
        print(
            f"Error: unknown project '{project_name}' (not found in {PROJECTS_YAML})",
            file=sys.stderr,
        )
        sys.exit(1)
    return {project_name: projects[project_name]}


def find_missing_paths(selected: dict) -> list[str]:
    """Return an error message per project whose path doesn't exist."""
    errors = []
    for name, entry in selected.items():
        path = Path(entry["path"])
        if not path.is_dir():
            errors.append(f"  {name}: path '{path}' does not exist or is not a directory")
    return errors


def find_bad_splice_targets(selected: dict, templates: list) -> list[str]:
    """Return an error message per project/splice-template whose output file is
    missing, or exists but has no standalone boundary line to splice against.
    Only checks projects whose path already passed find_missing_paths."""
    errors = []
    for name, entry in selected.items():
        out_dir = Path(entry["path"])
        if not out_dir.is_dir():
            continue  # already reported by find_missing_paths
        for tmpl_entry in templates:
            if tmpl_entry.get("mode", "overwrite") != "splice":
                continue
            output_path = out_dir / tmpl_entry["output"]
            if not output_path.is_file():
                errors.append(f"  {name}: '{output_path}' does not exist (splice target must pre-exist)")
                continue
            try:
                split_at_boundary(output_path.read_text(encoding="utf-8"))
            except ValueError:
                errors.append(f"  {name}: '{output_path}' has no standalone '---' line to splice at")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render generated artefacts for one or all projects."
    )
    parser.add_argument("--project", help="Render only this project (default: render all)")
    args = parser.parse_args()

    projects = load_projects(PROJECTS_YAML)
    templates = load_templates(TEMPLATES_YAML)
    selected = select_projects(projects, args.project)

    # Phase 1: validate every target path exists, and every splice target is
    # ready to splice against, BEFORE writing anything -- so a single bad
    # path or missing boundary can't leave some projects updated and others
    # not.
    errors = find_missing_paths(selected)
    errors += find_bad_splice_targets(selected, templates)
    if errors:
        print(
            "Error: the following problem(s) were found. Nothing was rendered:",
            file=sys.stderr,
        )
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    # Phase 2: render and write, now that every target is known-good.
    for name, entry in selected.items():
        tags = entry["tags"]
        out_dir = Path(entry["path"])
        for tmpl_entry in templates:
            template_path = Path(tmpl_entry["template"])
            template_str = template_path.read_text(encoding="utf-8")
            rendered = render_project(name, tags, template_str)
            output_path = out_dir / tmpl_entry["output"]
            mode = tmpl_entry.get("mode", "overwrite")
            if mode == "splice":
                body = split_at_boundary(output_path.read_text(encoding="utf-8"))
                output_path.write_text(rendered + "\n---\n" + body, encoding="utf-8")
            else:
                output_path.write_text(rendered, encoding="utf-8")
            print(f"Rendered {output_path}")


if __name__ == "__main__":
    main()
