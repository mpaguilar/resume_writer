import pytest
from datetime import datetime
from resume_writer.resume_model import Certification

test_data = """
Issuer: BigCorp
Name: BigCorp Certified Widget Expert
Issued: 03/2020
"""


@pytest.fixture()
def block_lines():
    lines = test_data.split("\n")

    return_lines = []
    for line in lines:
        if line.startswith("##"):
            return_lines.append(line[1:])
        else:
            return_lines.append(line)

    return return_lines

def test_parse_certification_block(block_lines):
    _certification = Certification.parse(block_lines)
    assert _certification.issuer == "BigCorp"
    assert _certification.name == "BigCorp Certified Widget Expert"
    assert _certification.issued == datetime(2020, 3, 1)
