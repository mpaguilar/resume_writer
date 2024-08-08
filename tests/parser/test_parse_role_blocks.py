from datetime import datetime

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
Agency: High-end 3rd party
Job category: Worker
Employment type: Contract
Start date: 01/2023
End date: 01/2024
Title: Senior Worker
Reason for change: Searching for new opportunities
Location: remote

### Summary
Performed senior tasks

### Responsibilities
Performed activities associated with a senior role.
Also did other things as required.

### Skills
* Skill 1
* Skill 2
* Skill 3

## Role

### Basics
Company: Example Company
Employment type: Full-time
Job category: Worker

Start date: 06/2020

End date: 06/2022

Title: Junior Worker

Reason for change: Laid off

Location: Somewhere, USA

### Summary
Performed junior tasks.

### Responsibilities
Performed routine activities associated with a junior role.
Other things were done as required.
* a thing
* another thing

### Skills

* Skill 1
* Skill 2
* Skill 4
"""

# subtract one to the line number to account for zero index
test_data_start_line = 14 - 1


def _block_lines():
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


def get_data_lines(first_line_number: int, last_line_number: int) -> list[str]:
    _data_start = (first_line_number - 1) - test_data_start_line
    _data_end = last_line_number - test_data_start_line
    _lines = _block_lines()[_data_start:_data_end]
    return _lines

#### End of common functions


def test_role_basics_block():
    _lines = get_data_lines(18, 38)
    _lines = _deindenter(_lines)
    _basics = RoleBasics.parse(_lines)

    assert isinstance(_basics, RoleBasics)
    assert _basics.company == "Another Company"
    assert _basics.start_date == datetime(2023, 1, 1, 0, 0)
    assert _basics.end_date == datetime(2024, 1, 1, 0, 0)
    assert _basics.title == "Senior Worker"
    assert _basics.reason_for_change == "Searching for new opportunities"
    assert _basics.location == "remote"
    assert _basics.employment_type == "Contract"
    assert _basics.job_category == "Worker"
    assert _basics.agency_name == "High-end 3rd party"


def test_summary_block():
    _lines = get_data_lines(29, 30)
    _lines = _deindenter(_lines)
    _summary = RoleSummary.parse(_lines)
    assert isinstance(_summary, RoleSummary)
    assert _summary.summary == "Performed senior tasks"


def test_responsibilities_block():
    _lines = get_data_lines(32, 33)
    _lines = _deindenter(_lines)
    _responsibilities = RoleResponsibilities.parse(_lines)
    assert isinstance(_responsibilities, RoleResponsibilities)
    assert (
        _responsibilities.text
        == "Performed activities associated with a senior role.\nAlso did other things as required."  # noqa: E501
    )


def test_skills_block():
    _lines = _deindenter(get_data_lines(36, 38))
    # remove blank lines
    _lines = [line for line in _lines if line]
    _skills = RoleSkills.parse(_lines)
    assert isinstance(_skills, RoleSkills)
    assert _skills.skills == ["Skill 1", "Skill 2", "Skill 3"]


def test_role_block():
    """Test one role."""
    _lines = _deindenter(get_data_lines(41, 70))
    # de-indent twice
    _block_lines = _deindenter(_lines)

    _role = Role.parse(_block_lines)
    assert isinstance(_role, Role)
    assert isinstance(_role.basics, RoleBasics)
    assert isinstance(_role.summary, RoleSummary)
    assert isinstance(_role.responsibilities, RoleResponsibilities)
    assert isinstance(_role.skills, RoleSkills)


def test_roles_block():
    """Test multiple roles."""
    _lines = _deindenter(get_data_lines(15, 70))
    _roles = Roles.parse(_lines)
    assert isinstance(_roles, Roles)
    assert len(_roles) == 2
    assert isinstance(_roles[0], Role)
    assert isinstance(_roles[1], Role)
