# TODO

*(Scratchpad for ideas, open decisions, quick wins -- resolved items move to `HISTORY.md`.)*

- [ ] Golden-file test: render `data/LLM_INSTRUCTIONS.md.j2` for real, against `project:scurry` + `technology:applescript`; check in the expected output by hand. Update only via deliberate re-approval when the template changes on purpose -- never auto-regenerate.
- [ ] Canonical bullet character in this project's docs/templates: use `-`, not `*`.
- [ ] Think about how to instruct LLMs to generate paragraphs without hard line breaks.
- [ ] Think about how to instruct LLMs to generate text with `--` instead of `—`.
- [ ] Revisit the `history:` dimension naming: `component:history` / `component:changelog` may read more clearly on first sight than `history:history` / `history:changelog` (the latter can look like a typo). Keeping current naming for now.
- [ ] Audit whether the fleet's various `LLM_INSTRUCTIONS.md` files still say "I want flow / good collaboration" enough -- this was a deliberate countermeasure against earlier model generations being hard to engage collaboratively, and shouldn't get lost in a future refactor focused on removing duplication.
- [ ] Longer-term, not scoped yet: manage `Makefile` / `pyproject.toml` variants (Windows-aware vs. not, package vs. script) through `stencil` the same way `LLM_INSTRUCTIONS.md` is handled.
- [ ] Minor/optional: a couple of inherited (pre-existing, not template-related) trailing-whitespace lines from the original `haddolib`/`scurry` prose were noted but left untouched. Cosmetic; clean up opportunistically.
- [ ] Minor/parked: whether the `## Technology Stack` sub-header line `**Scurry (macOS Automation):**` needs generalizing -- currently fine since it sits inside a blanket `project:scurry` wrap, but worth a second look if that wrap is ever split.
- [ ] Why do I need to have 2 empty lines at the end of the template to generate 1 empty line in the rendered file?