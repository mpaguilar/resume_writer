import pytest
from datetime import datetime
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    return [
        "# Degree",
        "School: University of College",
        "Degree: Masters of Baiters",
        "Started: 09/2015",
        "Ended: 05/2019",
        "# Degree",
        "School: University of Test",
        "Degree: Advanced Test Taker",
        "Started: 09/2020",
        "Ended: 05/2023",
    ]


def test_parse_education_block_correct_input(block_lines, resume_markdown):
    education = resume_markdown.parse_education_block(block_lines)
    degrees = education.degrees
    assert len(degrees) == 2

    # assertions for first degree
    assert degrees[0].degree == "Masters of Baiters"
    assert degrees[0].school == "University of College"
    assert degrees[0].start_date == datetime(2015, 9, 1)
    assert degrees[0].end_date == datetime(2019, 5, 1)

    # assertions for second degree
    assert degrees[1].degree == "Advanced Test Taker"
    assert degrees[1].school == "University of Test"
    assert degrees[1].start_date == datetime(2020, 9, 1)
    assert degrees[1].end_date == datetime(2023, 5, 1)


def test_parse_education_block_invalid_block_name(block_lines, resume_markdown):
    block_lines[0] = "Degreee"
    education = resume_markdown.parse_education_block(block_lines)
    degrees = education.degrees
    assert len(degrees) == 1


def test_parse_education_block_empty_input(resume_markdown):
    block_lines = []
    education = resume_markdown.parse_education_block(block_lines)
    assert len(education.degrees) == 0
