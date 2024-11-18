import pytest

from common import get_data_lines, deindenter  # type: ignore

from resume_writer.models.experience import (
    Roles,
)

from resume_writer.resume_render.skills_matrix import (
    career_experience_total,
    career_experience_span,
    skills_experience,
)

from resume_writer.models.parsers import ParseContext


test_data = """

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
"""

test_data_start_line = 17


@pytest.fixture
def roles():
    _lines = get_data_lines(test_data, test_data_start_line, 17, 75)
    data = deindenter(_lines, 2)

    _ctx = ParseContext(lines=data, doc_line_num=1)

    roles = Roles.parse(_ctx)
    return roles


def test_career_total(roles: Roles):
    assert isinstance(roles, Roles)
    years_of_experience = career_experience_total(roles)
    assert years_of_experience == 3


def test_career_span(roles: Roles):
    assert isinstance(roles, Roles)
    span_of_experience = career_experience_span(roles)
    assert span_of_experience == 3.6

def test_skills_experience(roles: Roles):
    assert isinstance(roles, Roles)
    skills_experience_matrix = skills_experience(roles)
    assert skills_experience_matrix == {
        "Skill 1": 3,
        "Skill 2": 3,
        "Skill 3": 1,
        "Skill 4": 2,
        }
