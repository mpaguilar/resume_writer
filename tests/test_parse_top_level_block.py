import pytest
from resume_writer.resume_markdown import MarkdownResumeParser
from resume_writer.resume_model import BasicBlockParse


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


class DummyClass(BasicBlockParse):
    def __init__(self, param1: str, section2: str):
        self.param1 = param1
        self.section2 = section2

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        return {"section 1": "param1", "section 2": "section2"}


def test_parse_basic_block_parse_blocks(block_lines):
    _blocks = DummyClass.parse_blocks(block_lines)
    assert _blocks == {
        "Section 1": ["Line 1", "Line 2"],
        "Section 2": ["Line 3", "# Subheader", "Line 4"],
    }


def test_parse_block_basic(block_lines):
    dummy = DummyClass.parse(block_lines=block_lines)
    assert dummy.param1 == "Section 1"
    assert dummy.section2 == "Section 2"


def test_top_level_blocks_empty_lines(resume_markdown):
    lines = ["", "  ", "\n", "\t"]
    dummy = DummyClass.parse_blocks(block_lines=lines)
    assert dummy == {}

