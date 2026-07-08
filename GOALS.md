# Project Goals & Roadmap

(Note: "I" in the following paragraphs refer to the user, "you" to you as the AI model.)

---

## 📍 Current Session Pointer

**Where we are:** Core rendering pipeline built and verified end-to-end against the real template. `data/projects.yaml` (`scurry`, `haddolib`) and `data/templates.yaml` populated; `scripts/render.py` (pure `render_project` + two-phase fail-loud `main()`, optional `--project` filter) wired into `make render`. Whitespace-quirk test suite green (10 tests, 4 fixture shapes: leading-dash trim, inline conditional, adjacent independent blocks, trailing-dash trim). `pyproject.toml` naming corrected.

**What's next:**
1. Golden-file test: render the real template against `project:scurry` + `technology:applescript`, hand-check the expected output. See `TODO.md`.
2. Decide real `path:` values for `scurry`/`haddolib` in `projects.yaml` -- currently `tmp/` placeholders; sibling-directory layout confirmed, but the switch hasn't been made.

---

## 🎯 Strategic vision

`stencil` keeps each project's generated artefacts (starting with `LLM_INSTRUCTIONS.md`, more to follow) in sync across an independent fleet of repos, without hand-editing each one. One Jinja2 template plus one `data/projects.yaml` -- flat `dimension:value` tags per project -- renders the right variant per repo. The template differentiates by *tag*, not by project identity: a new project is a `projects.yaml` entry, not a template fork. A new artefact type is a `templates.yaml` entry, applied uniformly to every project unless a future tag-gate (`requires:`) is added -- deliberately not built until an actual non-uniform case exists.
