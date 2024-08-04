import pytest

from models.resume import Resume
from models.personal import ContactInfo, Websites, VisaStatus, Banner, Note
from models.education import Degrees, Education
from models.certifications import Certifications
from models.roles import Roles


test_data = """
# Personal

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

# Education

## Degrees

### Degree
School: University of Example
Degree: Impressive Degree
Started: 08/1990
Ended: 05/1994

### Degree
School: University of College
Degree: Less Impressive Degree
Started: 08/1986
Ended: 05/1989

# Certifications

## Certification

Issuer: BigCorp
Name: BigCorp Certified Widget Expert
Issued: 03/2020
Expires: 03/2025

## Certification
Issuer: BigCorp
Name: BigCorp Certified Thing Expert
Issued: 04/2020
Expires: 04/2025

# Work history

## Role

### Basics
Company: Another Company
Start date: 01/2023
End date: 01/2024
Title: Senior Worker

Reason for change: Searching for new opportunities

### Description
Performed senior tasks

### Responsibilities
Performed activities associated with a senior role.

### Skills
* Skill 1
* Skill 2
* Skill 3

## Role

### Basics
Company: Example Company

Start date: 06/2020

End date: 06/2022

Title: Junior Worker

Reason for change: Laid off

### Description
Performed junior tasks.

### Responsibilities
Performed routine activities associated with a junor role.

### Skills

* Skill 1
* Skill 2
* Skill 4
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
    return lines


def test_parse_resume_complete(block_lines):
    resume = Resume.parse(block_lines)
    assert isinstance(resume, Resume)

    assert isinstance(resume.personal.contact_info, ContactInfo)
    assert isinstance(resume.personal.websites, Websites)
    assert isinstance(resume.personal.visa_status, VisaStatus)
    assert isinstance(resume.personal.banner, Banner)
    assert isinstance(resume.personal.note, Note)

    assert isinstance(resume.certifications, Certifications)
    assert len(resume.certifications) == 2

    assert isinstance(resume.education, Education)
    assert isinstance(resume.education.degrees, Degrees)
    assert len(resume.education.degrees) == 2

    assert isinstance(resume.roles, Roles)
    assert len(resume.roles) == 2
