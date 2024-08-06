from datetime import datetime

import pytest

from resume_writer.models.roles import (
    Role,
    Roles,
    RoleBasics,
    RoleSummary,
    RoleSkills,
    RoleResponsibilities,
)

test_data = """
## Role

### Basics
Company: Another Company
Start date: 01/2023
End date: 01/2024
Title: Senior Worker

Reason for change: Searching for new opportunities

### Summary
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


@pytest.fixture()
def block_lines():
    lines = test_data.split("\n")

    return_lines = []
    for line in lines:
        if line.startswith("# "):
            return_lines.append(line[1:])
        else:
            return_lines.append(line)

    return return_lines


def _deindenter(lines):
    _lines = []
    for _line in lines:
        if _line.startswith("##"):
            _line = _line[1:]
            _lines.append(_line)
        else:
            _lines.append(_line)
    return _lines


def test_role_basics_block(block_lines):
    _lines = _deindenter(block_lines[4:10])

    _basics = RoleBasics.parse(_lines)
    assert isinstance(_basics, RoleBasics)
    assert _basics.company == "Another Company"
    assert _basics.start_date == datetime(2023, 1, 1, 0, 0)
    assert _basics.end_date == datetime(2024, 1, 1, 0, 0)
    assert _basics.title == "Senior Worker"
    assert _basics.reason_for_change == "Searching for new opportunities"


def test_summary_block(block_lines):
    _lines = _deindenter(block_lines[12:14])
    # remove blank lines
    _lines = [line for line in _lines if line]
    _summary = RoleSummary.parse(_lines)
    assert isinstance(_summary, RoleSummary)
    assert _summary.summary == "Performed senior tasks"


def test_responsibilities_block(block_lines):
    _lines = _deindenter(block_lines[15:17])
    # remove blank lines
    _lines = [line for line in _lines if line]
    _responsibilities = RoleResponsibilities.parse(_lines)
    assert isinstance(_responsibilities, RoleResponsibilities)
    assert (
        _responsibilities.text
        == "Performed activities associated with a senior role."
    )


def test_skills_block(block_lines):
    _lines = _deindenter(block_lines[18:22])
    # remove blank lines
    _lines = [line for line in _lines if line]
    _skills = RoleSkills.parse(_lines)
    assert isinstance(_skills, RoleSkills)
    assert _skills.skills == ["Skill 1", "Skill 2", "Skill 3"]


def test_role_block(block_lines):
    """Test one role."""
    _block_lines = _deindenter(block_lines[2:21])
    # de-indent twice
    _block_lines = _deindenter(_block_lines)

    _role = Role.parse(_block_lines)
    assert isinstance(_role, Role)
    assert isinstance(_role.basics, RoleBasics)
    assert isinstance(_role.summary, RoleSummary)
    assert isinstance(_role.responsibilities, RoleResponsibilities)
    assert isinstance(_role.skills, RoleSkills)


def test_roles_block(block_lines):
    """Test multiple roles."""
    _lines = _deindenter(block_lines)
    _roles = Roles.parse(_lines)
    assert isinstance(_roles, Roles)
    assert len(_roles) == 2
    assert isinstance(_roles[0], Role)
    assert isinstance(_roles[1], Role)
