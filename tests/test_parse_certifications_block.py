import pytest
from datetime import datetime
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    return [
        "# Certification",
        "Name: Python Certification",
        "Issuer: Python Institute",
        "Issued: 01/2022",
        "# Certification",
        "Name: Machine Learning Certification",
        "Issuer: Python Institute",
        "Issued: 01/2022",
    ]


def test_parse_certifications_block_single_certification(resume_markdown, block_lines):
    block_lines = block_lines[:4]  # Only take the first certification block
    certifications = resume_markdown.parse_certifications_block(block_lines)
    assert len(certifications) == 1
    assert certifications[0].name == "Python Certification"
    assert certifications[0].issuer == "Python Institute"
    assert certifications[0].issued == datetime.strptime("01/2022", "%m/%Y")  # noqa: DTZ007


def test_parse_certifications_block_multiple_certifications(
    resume_markdown,
    block_lines,
):
    certifications = resume_markdown.parse_certifications_block(block_lines)

    assert len(certifications) == 2  # noqa: PLR2004
    assert certifications[0].name == "Python Certification"
    assert certifications[1].name == "Machine Learning Certification"


def test_parse_certifications_block_no_certifications(resume_markdown):
    block_lines = ["Some other section: blahblahblah", "Some info"]
    certifications = resume_markdown.parse_certifications_block(block_lines)
    assert len(certifications) == 0


def test_parse_certifications_block_invalid_date_format(resume_markdown, block_lines):
    block_lines[3] = "Issued: 01-2022"

    with pytest.raises(
        ValueError,
        match="time data '01-2022' does not match format '%m/%Y'",
    ):
        resume_markdown.parse_certifications_block(block_lines)
