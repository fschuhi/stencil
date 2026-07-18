# TODO

(Note: "I" in the following paragraphs refer to the user, "you" to you as the AI model.)

## Charter 
- Forward-looking only -- concrete, startable work: tasks specified well enough that next-session-me can begin within ten minutes, plus investigation items, test specs, and scratchpad ideas awaiting promotion or deletion.
- Items are unordered within their theme sections; open questions are marked _Needs investigation_ in the bullet.
- When an item is completed, record its durable outcome in `HISTORY.md` during the same session while the evidence and rationale are fresh, then strike it through in `TODO.md` with a concise handover note.
- Retain struck-through items through the next session because `TODO.md` is included in the standard filesdump while `HISTORY.md` normally is not; at the end of that next session, remove the already-archived items from `TODO.md`. Strategic direction, ordering, and milestones live in `GOALS.md` -- anything that needs a strategy discussion before it is actionable goes there.
- Architecture, contract, and settled decisions live in `README.md`.

---

- **Golden-file test:** render `data/LLM_INSTRUCTIONS.md.j2` for real, against `project:scurry` + `technology:applescript`; check in the expected output by hand. Update only via deliberate re-approval when the template changes on purpose -- never auto-regenerate.
- **Canonical bullet character in this project's docs/templates:** use `-`, not `*`.
- Think about how to instruct LLMs to generate paragraphs without hard line breaks.
- Think about how to instruct LLMs to generate text with `--` instead of `—`.
- **Revisit the `history:` dimension naming:** `component:history` / `component:changelog` may read more clearly on first sight than `history:history` / `history:changelog` (the latter can look like a typo). Keeping current naming for now.
- Audit whether the fleet's various `LLM_INSTRUCTIONS.md` files still say "I want flow / good collaboration" enough -- this was a deliberate countermeasure against earlier model generations being hard to engage collaboratively, and shouldn't get lost in a future refactor focused on removing duplication.
- Longer-term, not scoped yet: manage `Makefile` / `pyproject.toml` variants (Windows-aware vs. not, package vs. script) through `stencil` the same way `LLM_INSTRUCTIONS.md` is handled.
- Minor/optional: a couple of inherited (pre-existing, not template-related) trailing-whitespace lines from the original `haddolib`/`scurry` prose were noted but left untouched. Cosmetic; clean up opportunistically.
- Minor/parked: whether the `## Technology Stack` sub-header line `**Scurry (macOS Automation):**` needs generalizing -- currently fine since it sits inside a blanket `project:scurry` wrap, but worth a second look if that wrap is ever split.
- Why do I need to have 2 empty lines at the end of the template to generate 1 empty line in the rendered file?