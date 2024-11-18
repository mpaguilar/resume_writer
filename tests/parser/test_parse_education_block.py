from datetime import datetime

from resume_writer.models.education import Education, Degrees, Degree
from resume_writer.models.parsers import ParseContext

test_data = """
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
"""

# subtract one to the line number to account for zero index
test_data_start_line = 5 - 1 # line number of the first line of the test data


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


def test_parse_degree_block():
    _lines = get_data_lines(7, 15)
    _lines = _deindenter(_lines)

    _ctx = ParseContext(_lines, doc_line_num=7)

    degree = Degree.parse(_ctx)
    assert isinstance(degree, Degree)
    assert degree.school == "University of Example"
    assert degree.degree == "Impressive Degree"
    assert degree.start_date == datetime(1990, 8, 1)
    assert degree.end_date == datetime(1994, 5, 1)
    assert degree.major == "Example Major"
    assert degree.gpa == "3.5"
    assert _ctx.doc_line_num == 16

def test_parse_multiple_degrees_blocks():
    _lines = get_data_lines(8, 23)
    _lines = _deindenter(_lines)
    _lines = _deindenter(_lines) # needs two so "# Degree" is top-level

    _ctx = ParseContext(_lines, doc_line_num=8)

    degrees = Degrees.parse(_ctx)
    assert isinstance(degrees, Degrees)
    assert len(degrees.degrees) == 2
    assert degrees.degrees[0].school == "University of Example"
    assert degrees.degrees[1].school == "University of College"
    assert _ctx.doc_line_num == 24

def test_parse_education_block():
    _lines = get_data_lines(5, 23)
    _lines = _deindenter(_lines)

    _ctx = ParseContext(_lines, doc_line_num=5)

    education = Education.parse(_ctx)
    assert isinstance(education, Education)
    assert len(education.degrees.degrees) == 2
    assert education.degrees.degrees[0].school == "University of Example"
    assert education.degrees.degrees[1].school == "University of College"
    assert _ctx.doc_line_num == 24
