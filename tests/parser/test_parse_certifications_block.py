from datetime import datetime

import pytest
from resume_writer.models.certifications import Certification

test_data = """
## Certification

Issuer: BigCorp
Name: BigCorp Certified Widget Expert
Issued: 03/2020
Expires: 03/2025
Certification ID: 1234567890

## Certification
Issuer: BigCorp
Name: BigCorp Certified Thing Expert
Issued: 04/2020
Expires: 04/2025
Certification ID: 0987654321


"""
test_data_start_line = 6

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


@pytest.fixture
def block_lines():
    lines = test_data.split("\n")
    return _deindenter(lines)


def test_parse_certification_block():
    _lines = get_data_lines(9, 13)
    cert = Certification.parse(_lines)
    assert cert.issuer == "BigCorp"
    assert cert.name == "BigCorp Certified Widget Expert"
    assert cert.issued == datetime(2020, 3, 1)
    assert cert.expires == datetime(2025, 3, 1)
    assert cert.certification_id == "1234567890"
