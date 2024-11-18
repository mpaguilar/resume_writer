from resume_writer.models.experience import (
    Experience,
)
from resume_writer.models.parsers import ParseContext

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

test_data_start_line = 5


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


def test_basic_experience():
    _lines = get_data_lines(10, 107)
    _lines = _deindenter(_lines, 1)

    _ctx = ParseContext(lines=_lines, doc_line_num=10)

    _experience = Experience.parse(_ctx)
    assert isinstance(_experience, Experience)
    assert _ctx.doc_line_num == 108
