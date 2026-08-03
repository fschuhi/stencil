# stencil -- History

(Note: "I" in the following paragraphs refer to the user, "you" to you as the AI model.)

- The resolved-work record: what was built and when (note date, or have the points in roughly reverse-chronological order).
- This is the trophy case -- kept in the repo, **out of the per-session filesdump** (so it no longer rides along every session).
- For *forward* work see `TODO.md`; for direction see `GOALS.md`; for the architecture as it stands see `README.md`.
- See "Workflow for the Whole Session (CRITICAL)" in `LLM_INSTRUCTIONS.md` for the interplay between `TODO.md` and this file. 

---

- **2026-08-03 -- Partial-file templating for charters/preambles.** `TODO.md`, `GOALS.md`, `HISTORY.md` now get their generic charter sections (everything above the first standalone `---` line) rendered from `data/TODO.md.j2` / `data/GOALS.md.j2` / `data/HISTORY.md.j2` and spliced onto the hand-written body below, instead of being hand-copied per project. `render_project()` gained a `name` parameter, kept separate from `tags` since identity isn't a branching concern. `templates.yaml` entries now declare an explicit `mode: overwrite` or `mode: splice`. A new pure `split_at_boundary()` function implements "first standalone `---` line wins," resolving both open sub-questions the old Preamble management TODO posed: the title is part of the templated charter, and the `---` boundary is owned by the splice logic, not the template. Canonical titles settled as `# {{ name }} -- <Kind>` (e.g. `# stencil -- TODO`), closing the separate Canonical titles TODO too. A new fail-loud pre-flight check (`find_bad_splice_targets`) aborts the whole run, writing nothing, if any splice target is missing or lacks the boundary line. Verified by re-splicing each charter template against `stencil`'s own real files (byte-identical except the intended title change) and an end-to-end smoke test covering both the happy path and the fail-loud abort.