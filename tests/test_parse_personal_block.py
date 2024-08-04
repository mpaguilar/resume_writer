import pytest
from resume_writer.models.personal import (
    ContactInfo,
    Websites,
    VisaStatus,
    Banner,
    Note,
    Personal,
)

test_data = """
## Contact Information
Name: John Doe
Email: johndoe@example.com
Phone: 123-456-7890
Location: Somewhere, USA

## Websites
GitHub: https://github.com/example
LinkedIn: https://www.linkedin.com/in/example
Website: https://www.example.com
Twitter: https://twitter.com/example

## Visa Status
Work Authorization: US Citizen
Require sponsorship: No


## Banner

Experienced Widget Expert with a lot of experience in the field.

## Note

Proficent in the skills employers look for.
Lots of experience.
"""


def _deindenter(lines):
    _lines = []
    for _line in lines:
        if _line.startswith("##"):
            _line = _line[1:]
            _lines.append(_line)
        else:
            _lines.append(_line)
    return _lines


@pytest.fixture()
def block_lines():
    lines = test_data.split("\n")
    return _deindenter(lines)


def test_parse_personal_contact_info(block_lines):
    _lines = block_lines[2:6]
    contact_info = ContactInfo.parse(_lines)
    assert contact_info.name == "John Doe"
    assert contact_info.email == "johndoe@example.com"
    assert contact_info.phone == "123-456-7890"
    assert contact_info.location == "Somewhere, USA"


def test_parse_personal_websites(block_lines):
    _lines = block_lines[8:13]
    websites = Websites.parse(_lines)
    assert websites.github == "https://github.com/example"
    assert websites.linkedin == "https://www.linkedin.com/in/example"
    assert websites.website == "https://www.example.com"
    assert websites.twitter == "https://twitter.com/example"


def test_parse_personal_websites_missing_field(block_lines):
    _lines = block_lines[9:13]  # skil first line, github
    websites = Websites.parse(_lines)
    assert websites.github is None
    assert websites.linkedin == "https://www.linkedin.com/in/example"
    assert websites.website == "https://www.example.com"
    assert websites.twitter == "https://twitter.com/example"


def test_parse_personal_websites_missing_label(block_lines):
    _lines = block_lines[8:13]  # skip first line, github
    _lines[0] = "Github:"
    websites = Websites.parse(_lines)
    assert websites.github is None
    assert websites.linkedin == "https://www.linkedin.com/in/example"
    assert websites.website == "https://www.example.com"
    assert websites.twitter == "https://twitter.com/example"

def test_parse_personal_websites_missing_colon_on_label(block_lines):
    _lines = block_lines[8:13]  # skip first line, github
    _lines[0] = "Github"
    websites = Websites.parse(_lines)
    assert websites.github is None
    assert websites.linkedin == "https://www.linkedin.com/in/example"
    assert websites.website == "https://www.example.com"
    assert websites.twitter == "https://twitter.com/example"

def test_parse_visa_status(block_lines):
    _lines = block_lines[14:17]
    visa_status = VisaStatus.parse(_lines)
    assert visa_status.work_authorization == "US Citizen"
    assert visa_status.require_sponsorship is False

    _lines[1] = ""
    visa_status = VisaStatus.parse(_lines)
    assert visa_status.require_sponsorship is None


def test_parse_banner(block_lines):
    _lines = block_lines[19:22]
    banner = Banner.parse(_lines)
    assert (
        banner.text
        == "Experienced Widget Expert with a lot of experience in the field."
    )


def test_parse_note(block_lines):
    _lines = block_lines[24:27]
    note = Note.parse(_lines)
    assert (
        note.text == "Proficent in the skills employers look for.\nLots of experience."
    )


def test_parse_full_personal_block(block_lines):
    personal = Personal.parse(block_lines)
    assert isinstance(personal, Personal)
    assert isinstance(personal.contact_info, ContactInfo)
    assert isinstance(personal.websites, Websites)
    assert isinstance(personal.visa_status, VisaStatus)
    assert isinstance(personal.banner, Banner)



