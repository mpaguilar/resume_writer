from datetime import datetime

from resume_writer.models.experience import (
    ProjectOverview,
    ProjectDescription,
    ProjectSkills,
    Project,
)

test_data = """
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

"""

test_data_start_line = 10
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
    _lines = _lines[_data_start:_data_end + 1] # add one to include the last line
    return _lines


#### End of common functions


def test_project_overview_block():
    _lines = get_data_lines(15, 20)

    _overview = ProjectOverview.parse(_lines)
    assert isinstance(_overview, ProjectOverview)

    # test the values
    assert _overview.title == "A Useful project"
    assert _overview.url == "https://example.com/useful1"
    assert _overview.url_description == "A Useful Project"
    assert _overview.start_date == datetime(2020, 1, 1)
    assert _overview.end_date == datetime(2021, 1, 1)


def test_description_block():
    _lines = get_data_lines(22, 27)
    _lines = _deindenter(_lines)

    _description = ProjectDescription.parse(_lines)
    assert isinstance(_description, ProjectDescription)
    _text = """This should still be pretty short, 2-3 sentences.
Multiple lines are fine.

So are multiple paragraphs."""
    assert (
        _description.text
        == _text
    )


def test_skills_block():
    _lines = get_data_lines(29, 31)
    _skills = ProjectSkills.parse(_lines)
    assert isinstance(_skills, ProjectSkills)
    assert _skills.skills == ["Skill 1", "Skill 2", "Skill 5"]


def test_project_block():
    _lines = get_data_lines(13, 32)
    _lines = _deindenter(_lines, 3)

    _project = Project.parse(_lines)
    assert isinstance(_project, Project)
    assert isinstance(_project.overview, ProjectOverview)
    assert isinstance(_project.description, ProjectDescription)
    assert isinstance(_project.skills, ProjectSkills)
