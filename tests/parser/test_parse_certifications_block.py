from datetime import datetime

import pytest
from models.certifications import Certification

test_data = """
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


def test_parse_certification_block(block_lines):
    _lines = block_lines[3:7]
    cert = Certification.parse(_lines)
    assert cert.issuer == "BigCorp"
    assert cert.name == "BigCorp Certified Widget Expert"
    assert cert.issued == datetime(2020, 3, 1)
    assert cert.expires == datetime(2025, 3, 1)
