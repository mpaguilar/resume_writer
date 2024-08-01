import pytest
from resume_model import PersonalInfo

test_data = """
## Info
Name: John Doe
Email: johndoe@example.com
Phone: 123-456-7890

GitHub: https://github.com/example
LinkedIn: https://www.linkedin.com/in/example
Website: https://www.example.com
Work Authorization: US Citizen
Require sponsorship: No
Location: Somewhere, USA

## Banner

Experienced Widget Expert with a lot of experience in the field.

## Note

Proficent in the skills employers look for.
Lots of experience.
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

def test_parse_personal_info_block_valid_input(block_lines):
    personal = PersonalInfo.parse_labels(block_lines)
    assert isinstance(personal, PersonalInfo)
    assert personal.name == "John Doe"
    assert personal.email == "johndoe@example.com"
    assert personal.phone == "123-456-7890"
    assert personal.github == "https://github.com/example"
    assert personal.linkedin == "https://www.linkedin.com/in/example"
    assert personal.website == "https://www.example.com"
    assert personal.work_authorization == "US Citizen"
    assert personal.require_sponsorship == "No"
    assert personal.location == "Somewhere, USA"

def test_parse_personal_info_block_missing_fields(block_lines):

    _lines = [line for line in block_lines if not line.lower().startswith("email:")]
    personal = PersonalInfo.parse(_lines)
    assert personal.email is None
