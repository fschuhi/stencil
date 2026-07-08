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


def render_project(tags: list[str], template_str: str) -> str:
    """Pure rendering step: tags in, rendered text out. No file I/O here."""
    template = jinja2.Environment().from_string(template_str)
    return template.render(tags=tags)


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render generated artefacts for one or all projects."
    )
    parser.add_argument("--project", help="Render only this project (default: render all)")
    args = parser.parse_args()

    projects = load_projects(PROJECTS_YAML)
    templates = load_templates(TEMPLATES_YAML)
    selected = select_projects(projects, args.project)

    # Phase 1: validate every target path exists BEFORE writing anything,
    # so a single bad path can't leave some projects updated and others not.
    errors = find_missing_paths(selected)
    if errors:
        print(
            "Error: the following project path(s) do not exist. Nothing was rendered:",
            file=sys.stderr,
        )
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    # Phase 2: render and write, now that every target path is known-good.
    for name, entry in selected.items():
        tags = entry["tags"]
        out_dir = Path(entry["path"])
        for tmpl_entry in templates:
            template_path = Path(tmpl_entry["template"])
            template_str = template_path.read_text(encoding="utf-8")
            rendered = render_project(tags, template_str)
            output_path = out_dir / tmpl_entry["output"]
            output_path.write_text(rendered, encoding="utf-8")
            print(f"Rendered {output_path}")


if __name__ == "__main__":
    main()
