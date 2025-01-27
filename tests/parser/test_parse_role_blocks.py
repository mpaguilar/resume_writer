from datetime import datetime
import pytz

from resume_writer.models.experience import (
    Role,
    Roles,
    RoleBasics,
    RoleSummary,
    RoleSkills,
    RoleResponsibilities,
)

from resume_writer.models.parsers import ParseContext

test_data = """
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
"""

# subtract one to the line number to account for zero index
test_data_start_line = 12

# TODO: breaking up the test data is still a mess


def _block_lines():
    lines = test_data.split("\n")

    return_lines = []
    for line in lines:
        if line.startswith("# "):
            return_lines.append(line[1:])
        else:
            return_lines.append(line)

    return return_lines


def _deindenter(lines, count: int = 1):
    """Remove leading '#' from sub-blocks."""

    _lines = []
    for _ in range(count):
        _lines.clear()
        for _line in lines:
            if _line.startswith("##"):
                _line = _line[1:]
                _lines.append(_line)
            else:
                _lines.append(_line)
        lines = _lines.copy()

    return _lines


def get_data_lines(first_line_number: int, last_line_number: int) -> list[str]:
    _data_start = first_line_number - test_data_start_line
    _data_end = last_line_number - test_data_start_line
    _lines = _block_lines()
    _lines = _lines[_data_start : _data_end + 1]  # add one to include the last line
    return _lines


#### End of common functions


def test_role_basics_block():
    _lines = get_data_lines(18, 26)
    _ctx = ParseContext(_lines, doc_line_num=18)

    _basics = RoleBasics.parse(_ctx)

    assert isinstance(_basics, RoleBasics)
    assert _basics.company == "Another Company"
    assert _basics.start_date == datetime(2023, 1, 1, 0, 0).astimezone(pytz.utc)
    assert _basics.end_date == datetime(2024, 1, 1, 0, 0).astimezone(pytz.utc)
    assert _basics.title == "Senior Worker"
    assert _basics.reason_for_change == "Searching for new opportunities"
    assert _basics.location == "remote"
    assert _basics.employment_type == "Contract"
    assert _basics.job_category == "Worker"
    assert _basics.agency_name == "High-end 3rd party"
    assert _ctx.doc_line_num == 27  # (26 + 1, to account for zero index)


def test_summary_block():
    _lines = get_data_lines(29, 30)
    _ctx = ParseContext(_lines, doc_line_num=29)
    _summary = RoleSummary.parse(_ctx)
    assert isinstance(_summary, RoleSummary)
    assert _summary.summary == "Performed senior tasks"


def test_responsibilities_block():
    _lines = get_data_lines(32, 33)
    _ctx = ParseContext(_lines, doc_line_num=32)
    _responsibilities = RoleResponsibilities.parse(_ctx)
    assert isinstance(_responsibilities, RoleResponsibilities)
    assert (
        _responsibilities.text
        == "Performed activities associated with a senior role.\nAlso did other things as required."  # noqa: E501
    )
    assert _ctx.doc_line_num == 34  # (33 + 1, to account for zero index)


def test_skills_block():
    _lines = _deindenter(get_data_lines(36, 38))
    # remove blank lines
    _lines = [line for line in _lines if line]
    _ctx = ParseContext(_lines, doc_line_num=36)
    _skills = RoleSkills.parse(_ctx)
    assert isinstance(_skills, RoleSkills)
    assert _skills.skills == ["Skill 1", "Skill 2", "Skill 3"]
    assert _ctx.doc_line_num == 39  # (38 + 1, to account for zero index)


def test_role_block():
    """Test one role."""
    _lines = get_data_lines(41, 70)
    _block_lines = _deindenter(_lines, 3)

    _ctx = ParseContext(_block_lines, doc_line_num=41)

    _role = Role.parse(parse_context=_ctx)
    assert isinstance(_role, Role)
    assert isinstance(_role.basics, RoleBasics)
    assert isinstance(_role.summary, RoleSummary)
    assert isinstance(_role.responsibilities, RoleResponsibilities)
    assert isinstance(_role.skills, RoleSkills)
    assert _ctx.doc_line_num == 71  # (70 + 1, to account for zero index)


def test_roles_block():
    """Test multiple roles."""
    _lines = get_data_lines(15, 72)
    _lines = _deindenter(_lines, 2)
    _ctx = ParseContext(_lines, 0)
    _roles = Roles.parse(_ctx)
    assert isinstance(_roles, Roles)
    assert len(_roles) == 2
    assert isinstance(_roles[0], Role)
    assert isinstance(_roles[1], Role)
