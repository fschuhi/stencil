# stencil — Handover Note

Seed document for a fresh session. Distilled decisions, not a transcript.

## What `stencil` is

A fleet-management project that renders per-project `LLM_INSTRUCTIONS.md` files
from one Jinja2 template + one YAML data file, so additions like "Scope
Skepticism" only need to be written once and propagate to every project
instead of drifting apart by hand.

## Status

- **Step 1 (scaffold) — done.** `data/`, `scripts/`, `tmp/` (gitignored),
  `Makefile` (based on the `clip-tools` version, no editable-install step —
  `stencil` is a script, not an importable package), `pyproject.toml`
  (tooling config only, no `[build-system]`/packaging section).
  **Check:** confirm `pyproject.toml`'s `name` field was corrected to
  `"stencil"` (it briefly said `"unitum"`, a leftover from before naming
  settled) and that the packaging cleanup was actually applied — this was
  proposed but not explicitly confirmed as applied in the session that
  produced this handover.
- **Step 3 (template content) — done.** `LLM_INSTRUCTIONS.md.j2` (attached
  alongside this note) is content-complete, built from `haddolib`'s
  `LLM_INSTRUCTIONS.md` as baseline plus `scurry`'s deltas, reviewed
  section-by-section against a synopsis spreadsheet, and whitespace-verified
  by actually rendering both branches (not just read).
- **Step 2 (populate `data/projects.yaml`) — not started.**
- **Step 4 (`render.py` + Makefile wiring) — not started.**
- **Step 5 (tests) — not started.** Agreed to write these *early*, alongside
  a minimal fixture template, before feeding it the real content — see
  "Testing strategy" below.

## Architecture decisions

- **Two independent tag dimensions so far:** `technology:*` (e.g.
  `technology:python`, `technology:applescript`) and `project:*` (e.g.
  `project:scurry`). Two more were named as likely future dimensions but
  not yet used: `status:*` (private/public) and `components:*`
  (changelog/handover/etc.).
- **Tags are a flat list, namespaced with a `dimension:value` prefix** —
  not nested YAML, not separate lists per dimension. Cheap and greppable.
- **One combined `data/projects.yaml`**, one top-level key per project — not
  one YAML file per project. Chosen for eyeball-ability at this fleet size
  (currently ~2 handfuls of projects).
- **Omit tags rather than marking `components:none`** when a dimension
  doesn't apply to a project.
- **Plain `{% if %}` blocks, not `{% elif %}` chains** — even where a chain
  would be shorter — because independent `if` blocks don't assume mutual
  exclusivity, which is the safer default as the fleet grows.
- **Tag content by what it's actually about, not by what section it
  happens to sit in.** E.g. "Error Handling"'s AppleScript example is
  tagged `project:scurry` (it's about scurry's mail-exporter domain), not
  `technology:applescript` (which would wrongly imply all AppleScript
  projects share that example).
- **Don't split a tag preemptively for a hypothetical second instance.**
  Architecture Skepticism's own "a structural layer whose real population
  is one is a smell" was applied to the tagging design itself: an entire
  block can stay under one blanket `project:scurry` wrap even where some
  of its content is arguably about AppleScript-in-general, until a second
  AppleScript project actually exists to justify splitting the tag.
- **`CRITICAL_RULES.md` is not yet part of the templated fleet** — still
  one hand-maintained file shared by all projects. Two small edits to it
  are pending from this session (see TODOs).

## Whitespace-control convention (Jinja2)

Established the hard way — worth reading before writing new conditional
blocks, not rediscovering by trial and error.

**Rule of thumb:** use `{%- if %}` / `{%- endif %}` (dash on the left only)
to eat a block's own leading newline. Keep blank lines and section dividers
(`---`) as **literal, unconditional text outside** the `if`/`endif`, never
try to manufacture correct spacing with dashes *inside* a conditional block —
that reliably over- or under-trims once blocks are adjacent or nested.

Bad (produces stray blank lines when the tag is false, and can glue lines
together with no separator at all if you overcorrect with `-%}` on a
closing tag):
```jinja
Some fixed line.
{% if 'project:scurry' in tags %}
- scurry-only bullet
{% endif %}

## Next Heading
```

Good:
```jinja
Some fixed line.
{%- if 'project:scurry' in tags %}
- scurry-only bullet
{%- endif %}

## Next Heading
```

For **inline** conditionals at the end of a content line (not on their own
line), put the leading space *inside* the `{% if %}` rather than outside it,
so a false branch doesn't leave a trailing space:
```jinja
- **Error Handling:** Fail gracefully.{% if 'project:scurry' in tags %} If an email has no subject, default to "Unknown".{% endif %}
```

**Always verify by actually rendering both branches** (and the "neither tag
matches" edge case) rather than trusting a read-through — several bugs this
session were invisible on inspection and only surfaced on render.

## Testing strategy (agreed, not yet implemented)

Tests belong early, not at the end — the render logic is small and pure
(tags in, text out), and it's exactly where the real failure mode lives:
a mistyped tag silently renders a section as empty, with nothing to catch
it but eyeballing. Plan: write `render.py` against a tiny fixture template
with a couple of fake tags and a first passing test *before* feeding it
`LLM_INSTRUCTIONS.md.j2`'s real content, so the real content is tested
against already-trusted plumbing.

## Open TODOs

1. Add a "tagging principles" section to `stencil`'s `README.md`,
   capturing: tag by what content is about (not by section), don't split a
   tag preemptively for a population of one, and the whitespace-control
   convention above.
2. Two pending edits to `CRITICAL_RULES.md` (Rule 5 area): add "New logic
   must pass the existing test suite before being marked complete," and
   extend the test-reminder bullet with "...especially before merging a
   branch."
3. Audit whether the fleet's various `LLM_INSTRUCTIONS.md` files still say
   "I want flow / good collaboration" enough — this was a significant,
   deliberate countermeasure against earlier model generations being hard
   to engage collaboratively, and shouldn't get lost in a refactor that's
   mostly focused on removing duplication.
4. Longer-term idea, not scoped yet: manage `Makefile` / `pyproject.toml`
   variants (Windows-aware vs. not, package vs. script) through `stencil`
   the same way `LLM_INSTRUCTIONS.md` is handled.
5. Minor/optional: several *inherited* (pre-existing, not template-related)
   trailing-whitespace lines from the original `haddolib`/`scurry` prose
   were noted but left untouched, e.g. `"See \`CRITICAL_RULES.md\`: "` and
   a doubled trailing space after `"documents"`. Cosmetic; clean up
   opportunistically if convenient.

## Not yet decided

- Final tag values/spelling for `status:*` and `components:*` — named as
  likely dimensions, never actually used in the template yet.
- Whether the `## Technology Stack` sub-header line `**Scurry (macOS
  Automation):**` needs any generalization — currently fine since it sits
  inside a blanket `project:scurry` wrap, but worth a second look if that
  wrap is ever split.
