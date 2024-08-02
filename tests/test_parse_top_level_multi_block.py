import pytest
from resume_writer.resume_markdown import MarkdownResumeParser

test_data = """
# Multi-line Blocks
## Data block
Some data in data block 1
## Data block
Some data in data block 2
"""

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


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")



def test_empty_input(resume_markdown):

    _res = resume_markdown.top_level_multi_blocks([])
    assert _res == []

