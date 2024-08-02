import pytest
from datetime import datetime

from resume_writer.models.education import Education, Degrees, Degree

test_data = """
# Education
## Degrees

### Degree
School: University of Example
Degree: Impressive Degree
Start Date: 08/1990
End Date: 05/1994

### Degree
School: University of College
Degree: Less Impressive Degree
Start Date: 08/1986
End Date: 05/1989
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


def test_parse_degree_block(block_lines):
    _lines = _deindenter(block_lines[5:9])
    degree = Degree.parse(_lines)
    assert isinstance(degree, Degree)
    assert degree.school == "University of Example"
    assert degree.degree == "Impressive Degree"
    assert degree.start_date == datetime(1990, 8, 1)
    assert degree.end_date == datetime(1994, 5, 1)

def test_parse_multiple_degrees_blocks(block_lines):
    _lines = _deindenter(block_lines[4:])
    degrees = Degrees.parse(_lines)
    assert isinstance(degrees, Degrees)
    assert len(degrees.degrees) == 2
    assert degrees.degrees[0].school == "University of Example"
    assert degrees.degrees[1].school == "University of College"

def test_parse_education_block(block_lines):
    _lines = block_lines[2:]
    education = Education.parse(_lines)
    assert isinstance(education, Education)
    assert len(education.degrees.degrees) == 2
    assert education.degrees.degrees[0].school == "University of Example"
    assert education.degrees.degrees[1].school == "University of College"
