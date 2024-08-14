import pytest

from resume_writer.models.resume import Resume
from resume_writer.models.personal import (
    ContactInfo,
    Websites,
    VisaStatus,
    Banner,
    Note,
)
from resume_writer.models.education import Degrees, Education
from resume_writer.models.certifications import Certifications
from resume_writer.models.experience import Experience


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

Proficient in the skills employers look for.
Lots of experience.

# Education

## Degrees

### Degree
School: University of Example
Degree: Impressive Degree
Start date: 08/1990
End date: 05/1994
Major: Example Major
GPA: 3.5

### Degree
School: University of College
Degree: Less Impressive Degree
Start date: 08/1986
End date: 05/1989
Major: Example Major
GPA: 4.0

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

# Experience

## Projects
### Project

#### Overview
Title: A Useful project
Url: https://example.com/useful1
Url Description: A Useful Project
Start date: 01/2020
End date: 01/2021

#### Description

This should still be pretty short, 2-3 sentences.
Multiple lines are fine.

So are multiple paragraphs.

#### Skills
* Skill 1
* Skill 2
* Skill 5

### Project

#### Overview
Title: Another Useful project
Url: https://example.com/useful2
Url Description: Another Useful Project
Start date: 02/2020
End date: 02/2021

#### Description

This should still be pretty short, 2-3 sentences.
Multiple lines are fine.

So are multiple paragraphs.

#### Skills
* Skill 3
* Skill 4
* Skill 5

## Roles

### Role

#### Basics
Company: Another Company
Agency: High-end 3rd party 
Job category: Worker
Employment type: Contract
Start date: 01/2023
End date: 01/2024
Title: Senior Worker
Reason for change: Searching for new opportunities
Location: remote

#### Summary
Performed senior tasks

#### Responsibilities
Performed activities associated with a senior role.
Also did other things as required.

#### Skills
* Skill 1
* Skill 2
* Skill 3

### Role

#### Basics
Company: Example Company
Employment type: Full-time
Job category: Worker

Start date: 06/2020

End date: 06/2022

Title: Junior Worker

Reason for change: Laid off

Location: Somewhere, USA

#### Summary
Performed junior tasks.

#### Responsibilities
Performed routine activities associated with a junior role.
Other things were done as required.
* a thing
* another thing

#### Skills

* Skill 1
* Skill 2
* Skill 4
"""  # noqa: W291


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

    assert isinstance(resume.experience, Experience)
    _experience = resume.experience
    assert len(_experience.roles) == 2
    assert len(_experience.projects) == 2
