import pytest
from resume_writer.resume_markdown import MarkdownResumeParser
from resume_writer.resume_model import LabelBlockParse

test_data = """
## Section
Label1: This is label one
Label 2: This is label two

"""


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    lines = test_data.split("\n")

    return_lines = []
    for line in lines:
        if line.startswith("##"):
            return_lines.append(line[1:])
        else:
            return_lines.append(line)

    return return_lines


class DummyClass(LabelBlockParse):
    def __init__(self, label1: str, label2: str):
        self.label1 = label1
        self.label2 = label2

    @staticmethod
    def expected_fields() -> dict[str, str]:
        return {"label1": "label1", "label 2": "label2"}


def test_basic_labels(block_lines):
    dummy = DummyClass.parse(block_lines)
    assert dummy.label1 == "This is label one"
    assert dummy.label2 == "This is label two"
