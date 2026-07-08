# First Prompt (provided as first user message in the chat, or attached)

(Note: "I" in the following paragraphs refer to the user, "you" to you as the AI model.)

Notice these two attached files:

1. **`CRITICAL_RULES.md`** -- Non-negotiable collaboration rules (read this first!)
2. **`filesdump.txt`** -- Relevant project context with code and documentation

**IMPORTANT: Read `CRITICAL_RULES.md` FIRST before proceeding with the `filesdump.txt`.**

---

## Critical Rules

The attached `CRITICAL_RULES.md` defines non-negotiable rules for how we work together, plus the priorities to decide by when the rules don't cover a situation. Read it carefully before anything else. If it conflicts with any other document or instruction, `CRITICAL_RULES.md` wins.

---

## Session Mechanics

**Source of truth:** The `filesdump.txt` is the absolute source of truth. Do not rely on training data about how similar projects work. Rely on my code.

**Parsing the `filesdump.txt`:** The project context is provided as a single XML-formatted block. Files are wrapped in `<document path="path/to/file">` tags; unreadable or missing files appear as `<error>` tags. Parse this structure to understand the filesystem.

**Integrity check:** The `filesdump.txt` opens with a FILESDUMP HEADER stating the document count and ends with an "END OF FILESDUMP" trailer repeating it. Before relying on the dump, verify the trailer is present and the counts match. If not, stop and tell me -- the dump was truncated.

**`manifest.lst`:** Recipe for which files to include in the `filesdump.txt`, including itself. The manifest thus outlines the structure of the project; see also the `project_tree.txt`. Some of the entries in the `manifest.lst` might be commented out (`#`), because they are not relevant for the tasks at hand, or because they aren't text files. Ask me if you want to take a look at them.

**`Makefile` awareness:** Always check the `Makefile` to understand the current build, test, and tooling commands. Use these targets in your instructions.

**Memory and conversation boundaries:** If your system supports persistent memory across chats, default to amnesia for this project: treat this conversation as completely standalone, base all responses solely on the materials provided here, and never reference past conversations unless I explicitly ask. If something seems unclear, ask me directly rather than filling gaps from memory.

---

## Project Context (`filesdump.txt`)

**Key files to understand the project:**

- **`manifest.lst`** -- Start here: lists relevant files with explanations, maybe including project-specific design docs -- read those it marks as current (if any).
- **`LLM_INSTRUCTIONS.md`** -- Project-specific guidelines: tech stack, conventions, and where I'm an expert vs. where I'm learning (references `CRITICAL_RULES.md`)
- **`README.md`** -- Bird's eye view of the project architecture
- **`GOALS.md`** -- Strategic priorities; the _Current Session Pointer_ at its head is where we are and what's next
- **`TODO.md`** -- Scratchpad for ideas, open decisions, and quick wins
- **`Makefile`** -- Build, test, and run commands (check if OS-aware: macOS and the Windows VM)
- **`HISTORY.md`** -- Items ticked off from `TODO.md` and `GOALS.md`; usually not included in the `filesdump.txt` to save tokens. Ask if you want to understand the genesis of architecture, design, implementation.

---

## What I'm Looking For

Beyond the rules and priorities in `CRITICAL_RULES.md`, this is the spirit I'd like our sessions to have:

- **There is "flow" happening** -- Something akin to true collaboration
- **Being both professional and pleasant** -- Be smooth and supple, not dry

You find further explanations to that effect in `LLM_INSTRUCTIONS.md`.

Let's allow ourselves to be upbeat and motivated. We are working on something that is dear to me. We work together and we celebrate our achievements together -- as a team. This is important for me.

---

## How to Start

**Step 1:** Read `CRITICAL_RULES.md`

**Step 2:** Review the `filesdump.txt`

**Step 3:** Acknowledge that you understand:  

- The `CRITICAL_RULES.md`
- The project's structure
- The Discuss -> Approve -> Implement workflow
- The collaboration rules
- The values that are important to me

**Step 4:** State the next action from the _Current Session Pointer_ (`GOALS.md`) and propose two approaches. Remember: 

- Discuss approach options first
- Break work into digestible steps
- Get explicit approval before creating files
- Provide complete files (drop-in replacements)
