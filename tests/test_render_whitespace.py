from pathlib import Path

import jinja2

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def render_fixture(name: str, tags: list[str]) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(FIXTURES_DIR))
    template = env.get_template(name)
    return template.render(tags=tags)


def test_leading_dash_trim_tag_present():
    result = render_fixture("leading_dash_trim.j2", tags=["demo:on"])
    expected = "Some fixed line.\n- demo bullet\n\n## Next Heading"
    assert result == expected


def test_leading_dash_trim_tag_absent():
    result = render_fixture("leading_dash_trim.j2", tags=[])
    expected = "Some fixed line.\n\n## Next Heading"
    assert result == expected


def test_inline_conditional_tag_present():
    result = render_fixture("inline_conditional.j2", tags=["demo:strict"])
    expected = "Error handling: fail-fast.\nNext line."
    assert result == expected


def test_inline_conditional_tag_absent():
    result = render_fixture("inline_conditional.j2", tags=[])
    expected = "Error handling: best-effort.\nNext line."
    assert result == expected


def test_adjacent_independent_ifs_both_present():
    result = render_fixture("adjacent_independent_ifs.j2", tags=["demo:alpha", "demo:beta"])
    expected = "Intro line.\n- alpha bullet\n- beta bullet\n\n## Closing Heading"
    assert result == expected


def test_adjacent_independent_ifs_only_alpha():
    result = render_fixture("adjacent_independent_ifs.j2", tags=["demo:alpha"])
    expected = "Intro line.\n- alpha bullet\n\n## Closing Heading"
    assert result == expected


def test_adjacent_independent_ifs_only_beta():
    result = render_fixture("adjacent_independent_ifs.j2", tags=["demo:beta"])
    expected = "Intro line.\n- beta bullet\n\n## Closing Heading"
    assert result == expected


def test_adjacent_independent_ifs_neither():
    result = render_fixture("adjacent_independent_ifs.j2", tags=[])
    expected = "Intro line.\n\n## Closing Heading"
    assert result == expected


def test_trailing_dash_trim_tag_present():
    result = render_fixture("trailing_dash_trim.j2", tags=["demo:on"])
    expected = "Header line.\n- trailing bullet\nFooter line."
    assert result == expected


def test_trailing_dash_trim_tag_absent():
    result = render_fixture("trailing_dash_trim.j2", tags=[])
    expected = "Header line.\nFooter line."
    assert result == expected
