import pytest
from resume_writer.resume_markdown import MarkdownResumeParser
from resume_model import Personal

test_data = """
## Info
Name: John Doe
Email: johndoe@example.com
Phone: 123-456-7890

GitHub: https://github.com/example
LinkedIn: https://www.linkedin.com/in/example
Website: https://www.example.com
Work Authorization: US Citizen
Requires sponsorship: No
Location: Somewhere, USA

## Banner

Experienced Widget Expert with a lot of experience in the field.

## Note

Proficent in the skills employers look for.
Lots of experience.
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


def test_parse_personal_block_valid_input(block_lines):
    personal = Personal.parse(block_lines)
    assert personal.personal_info is not None
    assert personal.banner == [
        "Experienced Widget Expert with a lot of experience in the field.",
    ]
    assert personal.note == [
        "Proficent in the skills employers look for.",
        "Lots of experience.",
    ]

def test_parse_personal_block_missing_block(block_lines):
    block_lines = block_lines[:12] + block_lines[15:]

    personal = Personal.parse(block_lines)
    assert personal.personal_info is not None
    assert personal.banner is None
    assert personal.note == [
        "Proficent in the skills employers look for.",
        "Lots of experience.",
    ]
