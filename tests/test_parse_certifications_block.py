import pytest
from resume_writer.resume_model import Certification, Certifications

test_data = """
# Certification

Issuer: BigCorp
Name: BigCorp Certified Widget Expert
Issued: 03/2020

# Certification
Issuer: BigCorp
Name: BigCorp Certified Thing Expert
Issued: 04/2020
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


def test_parse_certifications_block(block_lines):
    certifications = Certifications.parse(block_lines=block_lines)
    assert len(certifications) == 2
    assert all(
        isinstance(certification, Certification) for certification in certifications
    )
