#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

# XML Template for each file
FILE_TEMPLATE = """<document path="{path}">
{content}
</document>
"""

# XML Template for error markers (unreadable or missing files)
ERROR_TEMPLATE = """<error path="{path}">{reason}</error>
"""

# Header and trailer: declared expectations so the consuming model can detect
# a truncated or clipped dump. The header survives truncation (truncation eats
# the tail), so even a clipped dump states what it should have contained.
HEADER_TEMPLATE = """<!-- FILESDUMP HEADER: {count} document(s), ~{tokens:,} tokens.
     This dump ends with an 'END OF FILESDUMP' trailer stating the same
     document count. If the trailer is missing or the counts differ, the dump
     was truncated: stop and report instead of working from partial context. -->
"""

TRAILER_TEMPLATE = """<!-- END OF FILESDUMP: {count} document(s) included. -->
"""

# Literal boundary strings that must never occur inside file content: a file
# containing one of these would prematurely open or close a wrapper tag and
# silently corrupt the dump. The build fails hard on any collision.
# (Note: this script contains these strings itself, so it can never be
# included in a dump -- attach it to the prompt separately when needed.)
BOUNDARY_MARKERS = (
    "<documents>",
    "</documents>",
    "<document path=",
    "</document>",
    "<error path=",
)

# Rough heuristic: ~4 characters per token for typical code/prose mixes
CHARS_PER_TOKEN = 4

# Bytes per KB, for the --detailed per-file size report
BYTES_PER_KB = 1024


def concat(list_file: Path, out, detailed: bool = False, sort: bool = False):
    if not list_file.exists():
        out.write(f"Error: Cannot read file '{list_file}'\n")
        return 1

    try:
        # utf-8-sig handles potential BOMs
        lines = list_file.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError) as e:
        out.write(f"Error: Cannot read file '{list_file}': {e}\n")
        return 1

    included = 0
    errors = []      # (path, reason) tuples
    collisions = []  # (path, marker) tuples
    total_chars = 0
    # ("file", path, content, size_bytes) or ("error", path, reason)
    entries = []

    # Phase 1: read everything into memory. Buffering is required because the
    # header declares counts that are only known after all files are read.
    for raw in lines:
        name = raw.strip()

        # Skip empty lines and comments
        if not name or name.startswith("#"):
            continue

        p = Path(name)
        if p.exists() and p.is_file():
            try:
                content = p.read_text(encoding="utf-8")
                for marker in BOUNDARY_MARKERS:
                    if marker in content:
                        collisions.append((name, marker))
                size_bytes = p.stat().st_size
                entries.append(("file", name, content, size_bytes))
                included += 1
                total_chars += len(content)
            except (OSError, UnicodeDecodeError) as e:
                reason = f"Cannot read file: {e}"
                entries.append(("error", name, reason))
                errors.append((name, reason))
        else:
            reason = "File not found"
            entries.append(("error", name, reason))
            errors.append((name, reason))

    # Fail hard on boundary collisions: a poisoned dump is worse than no dump.
    # Nothing is written to stdout, so a shell redirection yields an empty file.
    if collisions:
        sys.stderr.write("concat_files: FAILED -- boundary marker collision(s):\n")
        for path, marker in collisions:
            sys.stderr.write(f"  {path}: contains literal '{marker}'\n")
        sys.stderr.write(
            "No dump written. Comment the offending file(s) out in the "
            "manifest; attach them to the prompt separately if needed.\n"
        )
        return 1

    est_tokens = total_chars // CHARS_PER_TOKEN

    # Phase 2: write the dump.
    # Optional: Escape XML special characters if necessary,
    # though LLMs are usually robust enough with raw code in these tags.
    # For strict correctness, one might wrap content in CDATA,
    # but simple tag wrapping is the current standard for prompts.
    out.write("<documents>\n")
    out.write(HEADER_TEMPLATE.format(count=included, tokens=est_tokens))
    for entry in entries:
        if entry[0] == "file":
            _, name, content, _size = entry
            out.write(FILE_TEMPLATE.format(path=name, content=content))
        else:
            _, name, reason = entry
            out.write(ERROR_TEMPLATE.format(path=name, reason=reason))
    out.write(TRAILER_TEMPLATE.format(count=included))
    out.write("</documents>\n")

    # Everything below goes to stderr, not stdout: stdout is reserved for the
    # dump itself so `... > filesdump.txt` redirection stays clean. This is
    # also why --detailed reports here rather than inline in the dump -- the
    # dump's content should only ever be what the manifest asked for.
    if detailed:
        file_entries = [e for e in entries if e[0] == "file"]
        if sort:
            # Descending by on-disk size; ties broken by name for determinism.
            file_entries.sort(key=lambda e: (-e[3], e[1]))
        label = " (sorted by size, descending)" if sort else ""
        sys.stderr.write(f"concat_files: per-file breakdown{label} ({included} file(s)):\n")
        for _, name, content, size_bytes in file_entries:
            tokens = len(content) // CHARS_PER_TOKEN
            kb = size_bytes / BYTES_PER_KB
            sys.stderr.write(f"  {name}: ~{tokens:,} tokens, {kb:,.1f} KB\n")

    # Summary to stderr (keeps stdout clean for redirection)
    sys.stderr.write(
        f"concat_files: {included} file(s) included, "
        f"{len(errors)} error(s), "
        f"~{est_tokens:,} tokens ({total_chars:,} chars)\n"
    )
    for path, reason in errors:
        sys.stderr.write(f"  ERROR {path}: {reason}\n")

    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="concat_files.py",
        description="Concatenate the files listed in a manifest into an XML-wrapped filesdump.",
    )
    parser.add_argument("filelist", type=Path, help="Path to the manifest file (e.g. manifest.lst)")
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Report each included file's name, token estimate, and size in KB on stderr.",
    )
    parser.add_argument(
        "-s", "--sort",
        action="store_true",
        help="With --detailed, sort the per-file breakdown by size, descending. No effect without --detailed.",
    )
    args = parser.parse_args(argv)

    if args.sort and not args.detailed:
        parser.error("--sort has no effect without --detailed")

    return concat(args.filelist, sys.stdout, detailed=args.detailed, sort=args.sort)


if __name__ == "__main__":
    sys.exit(main())
