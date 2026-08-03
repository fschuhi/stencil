from pathlib import Path

import pytest

from scripts.render import split_at_boundary

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_split_at_boundary_clean():
    text = read_fixture("split_boundary_clean.txt")
    result = split_at_boundary(text)
    assert result == "Body line one.\nBody line two.\n"


def test_split_at_boundary_missing_raises():
    text = read_fixture("split_boundary_missing.txt")
    with pytest.raises(ValueError):
        split_at_boundary(text)


def test_split_at_boundary_first_occurrence_wins():
    text = read_fixture("split_boundary_two_markers.txt")
    result = split_at_boundary(text)
    assert result == "Body line one.\n---\nBody line two still part of body.\n"


def test_split_at_boundary_no_false_match_on_partial_line():
    text = read_fixture("split_boundary_table_no_false_match.txt")
    result = split_at_boundary(text)
    assert result == "Actual body starts here.\n"
