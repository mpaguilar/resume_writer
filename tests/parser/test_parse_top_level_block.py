import pytest


from resume_writer.models.parsers import TextBlockParse, BasicBlockParse

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


class DummyTextClass(TextBlockParse):
    def __init__(self, text: str):
        self.text = text


class DummyClass(BasicBlockParse):
    def __init__(self, param1: str, section2: str):
        self.param1 = param1
        self.section2 = section2

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        return {"section 1": "param1", "section 2": "section2"}

    @staticmethod
    def block_classes() -> dict[str, type]:
        return {"section 1": DummyTextClass, "section 2": DummyTextClass}


def test_parse_basic_block_parse_blocks(block_lines):
    _blocks = DummyClass.parse_blocks(block_lines)
    assert _blocks == {
        "section 1": ["Line 1", "Line 2"],
        "section 2": ["Line 3", "# Subheader", "Line 4"],
    }


def test_parse_block_basic(block_lines):
    dummy = DummyClass.parse(block_lines=block_lines)
    assert isinstance(dummy.param1, DummyTextClass)
    assert dummy.param1.text == "Line 1\nLine 2"
    assert isinstance(dummy.section2, DummyTextClass)
    assert dummy.section2.text == "Line 3\n# Subheader\nLine 4"


def test_top_level_blocks_empty_lines():
    lines = ["", "  ", "\n", "\t"]
    dummy = DummyClass.parse_blocks(block_lines=lines)
    assert dummy == {}
