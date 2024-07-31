import pytest
from resume_writer.resume_markdown import MarkdownResumeParser

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


def test_parse_personal_block_valid_input(resume_markdown, block_lines):
    personal = resume_markdown.parse_personal_block(block_lines)
    assert personal.personal_info.name == "John Doe"
    assert personal.personal_info.email == "johndoe@example.com"
    assert personal.personal_info.phone == "123-456-7890"
    assert (
        personal.banner
        == "Experienced Widget Expert with a lot of experience in the field."
    )
    assert (
        personal.note
        == "Proficent in the skills employers look for.\nLots of experience."
    )


