import pytest
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    return [
        "# Section 1",
        "Line 1",
        "",
        "Line 2",
        "# Section 2",
        "Line 3",
        "## Subheader",
        "Line 4",
    ]


def test_top_level_blocks_empty_lines(resume_markdown):
    lines = ["", "  ", "\n", "\t"]
    blocks = resume_markdown.top_level_blocks(lines)
    assert blocks == {}


def test_top_level_blocks_single_section(resume_markdown):
    lines = ["# Section", "Line 1", "Line 2"]
    blocks = resume_markdown.top_level_blocks(lines)
    assert blocks == {"Section": ["Line 1", "Line 2"]}


def test_top_level_blocks_multiple_sections(resume_markdown):
    lines = ["# Section 1", "Line 1", "# Section 2", "Line 2"]
    blocks = resume_markdown.top_level_blocks(lines)
    assert blocks == {"Section 1": ["Line 1"], "Section 2": ["Line 2"]}


def test_top_level_blocks_subheader(resume_markdown):
    lines = ["# Section", "Line 1", "## Subheader", "Line 2"]
    blocks = resume_markdown.top_level_blocks(lines)
    assert blocks == {"Section": ["Line 1", "# Subheader", "Line 2"]}


def test_top_level_blocks_mixed_lines(resume_markdown, block_lines):
    blocks = resume_markdown.top_level_blocks(block_lines)
    assert blocks == {
        "Section 1": ["Line 1", "Line 2"],
        "Section 2": ["Line 3", "# Subheader", "Line 4"],
    }
