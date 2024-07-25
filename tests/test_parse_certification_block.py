import pytest
from datetime import datetime
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def markdown_resume_parser():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    return ["Name: Certificate Name", "Issuer: Certificate Issuer", "Issued: 01/2022"]


def test_parse_certification_valid_input(markdown_resume_parser, block_lines):
    certification = markdown_resume_parser.parse_certification(block_lines)
    assert certification.name == "Certificate Name"
    assert certification.issuer == "Certificate Issuer"
    assert certification.issued == datetime(2022, 1, 1)  # noqa: DTZ001


def test_parse_certification_missing_name(markdown_resume_parser):
    block_lines = ["Issuer: Certificate Issuer", "Issued: 01/2022"]
    certification = markdown_resume_parser.parse_certification(block_lines)
    assert certification.name is None
    assert certification.issuer == "Certificate Issuer"
    assert certification.issued == datetime(2022, 1, 1)  # noqa: DTZ001


def test_parse_certification_missing_issuer(markdown_resume_parser):
    block_lines = ["Name: Certificate Name", "Issued: 01/2022"]
    certification = markdown_resume_parser.parse_certification(block_lines)
    assert certification.name == "Certificate Name"
    assert certification.issuer is None
    assert certification.issued == datetime(2022, 1, 1)  # noqa: DTZ001


def test_parse_certification_missing_issued_date(markdown_resume_parser):
    block_lines = ["Name: Certificate Name", "Issuer: Certificate Issuer"]
    certification = markdown_resume_parser.parse_certification(block_lines)
    assert certification.name == "Certificate Name"
    assert certification.issuer == "Certificate Issuer"
    assert certification.issued is None


def test_parse_certification_invalid_issued_date_format(markdown_resume_parser):
    block_lines = [
        "Name: Certificate Name",
        "Issuer: Certificate Issuer",
        "Issued: 01-2022",
    ]
    with pytest.raises(
        ValueError,
        match="time data '01-2022' does not match format '%m/%Y'",
    ):
        markdown_resume_parser.parse_certification(block_lines)


def test_parse_certification_empty_input(markdown_resume_parser):
    block_lines = []
    certification = markdown_resume_parser.parse_certification(block_lines)
    assert certification.name is None
    assert certification.issuer is None
    assert certification.issued is None
