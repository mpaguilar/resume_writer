import logging

import pytest
from datetime import datetime
from resume_writer.resume_markdown import MarkdownResumeParser

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture()
def sample_job_block():
    return [
        "# Basics",
        "Title: Software Engineer",
        "Company: Google",
        "Start date: 01/2018",
        "End date: 12/2020",
        "Reason for change: Moved to a new opportunity",
        "# Description",
        "Developed and maintained software applications.",
        "# Responsibilities",
        "Wrote all the code\nWrote all the tests.",
        "# Skills",
        "* Python",
        "* Pytest",
    ]


@pytest.fixture()
def resume_parser():
    return MarkdownResumeParser("dummy")


def test_parse_job_basics_block(resume_parser, sample_job_block):
    title, company, started, ended, reason = resume_parser.parse_job_basics_block(
        sample_job_block[1:6],
    )
    assert title == "Software Engineer"
    assert company == "Google"
    assert started == datetime(2018, 1, 1, 0, 0) #noqa: DTZ001
    assert ended == datetime(2020, 12, 1, 0, 0) #noqa: DTZ001
    assert reason == "Moved to a new opportunity"


def test_parse_job_block(resume_parser, sample_job_block):
    job = resume_parser.parse_role_block(sample_job_block)
    assert job.title == "Software Engineer"
    assert job.company == "Google"
    assert job.start_date == datetime(2018, 1, 1, 0, 0) #noqa: DTZ001
    assert job.end_date == datetime(2020, 12, 1, 0, 0) #noqa: DTZ001
    assert job.reason_for_change == "Moved to a new opportunity"
    assert job.description == "Developed and maintained software applications."
    assert (
        job.responsibilities
        == "Wrote all the code\nWrote all the tests."
    )
    assert job.skills == ["Python", "Pytest"]


def test_parse_job_block_empty_description(resume_parser, sample_job_block):
    sample_job_block[7:8] = []
    job = resume_parser.parse_role_block(sample_job_block)
    assert job.description is None


