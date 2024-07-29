import pytest
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")

@pytest.fixture()
def block_lines():
    return  [
        "# Info",
        "name: John Doe",
        "email: johndoe@example.com",
        "phone: 1234567890",
        "# Banner",
        "This is a banner",
        "# Note",
        "This is a note",
        "This is the second line of a note",
    ]

def test_parse_personal_block_valid_input(resume_markdown, block_lines):

    personal = resume_markdown.parse_personal_block(block_lines)
    assert personal.personal_info.name == "John Doe"
    assert personal.personal_info.email == "johndoe@example.com"
    assert personal.personal_info.phone == "1234567890"
    assert personal.banner == "This is a banner"
    assert personal.note == "This is a note\nThis is the second line of a note"


def test_parse_personal_block_missing_info(resume_markdown, block_lines):
    block_lines = block_lines[4:]
    personal = resume_markdown.parse_personal_block(block_lines)
    assert personal.personal_info.name is None
    assert personal.personal_info.email is None
    assert personal.personal_info.phone is None
    assert personal.banner == "This is a banner"
    assert personal.note == "This is a note\nThis is the second line of a note"


def test_parse_personal_block_empty_input(resume_markdown):
    block_lines = []
    personal = resume_markdown.parse_personal_block(block_lines)
    assert personal.personal_info.name is None
    assert personal.personal_info.email is None
    assert personal.personal_info.phone is None
    assert personal.banner is None
    assert personal.note is None
