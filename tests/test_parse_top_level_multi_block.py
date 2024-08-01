import pytest
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


def test_empty_input(resume_markdown):
    _res = resume_markdown.top_level_multi_blocks([])
    assert _res == []


def test_single_block(resume_markdown):
    lines = ["# Section", "Line 1", "Line 2"]
    assert resume_markdown.top_level_multi_blocks(lines) == [["Line 1", "Line 2"]]


def test_multiple_blocks(resume_markdown):
    lines = ["# Section1", "Line 1", "Line 2", "# Section2", "Line 3", "Line 4"]
    assert resume_markdown.top_level_multi_blocks(lines) == [
        ["Line 1", "Line 2"],
        ["Line 3", "Line 4"],
    ]


def test_empty_lines(resume_markdown):
    lines = ["# Section1", "Line 1", "", "Line 2", "# Section2", "Line 3", ""]
    assert resume_markdown.top_level_multi_blocks(lines) == [
        ["Line 1", "Line 2"],
        ["Line 3"],
    ]


def test_no_section_header(resume_markdown):
    lines = ["Line 1", "Line 2"]
    assert resume_markdown.top_level_multi_blocks(lines) == []


def test_section_header_only(resume_markdown):
    lines = ["# Section1", "# Section2"]
    assert resume_markdown.top_level_multi_blocks(lines) == []


def test_section_header_at_end(resume_markdown):
    lines = ["Line 1", "Line 2", "# Section1", "Line 3"]
    assert resume_markdown.top_level_multi_blocks(lines) == [["Line 3"]]
