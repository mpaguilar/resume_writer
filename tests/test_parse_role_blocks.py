from datetime import datetime
import pytest
from resume_writer.resume_markdown import MarkdownResumeParser


@pytest.fixture()
def resume_markdown():
    return MarkdownResumeParser("dummy")


@pytest.fixture()
def block_lines():
    return [
        "# Role",
        "## Basics",
        "Company: Google",
        "Start Date: 01/2020",
        "End Date: 01/2022",
        "Title: Senior Software Engineer",
        "Reason for change: Promoted to Manager",
        "## Description",
        "Developed a new feature for the company's flagship product",
        "## Responsibilities",
        "This is a paragraph.\n\nThis is another paragraph.",
        "## Skills",
        "* Python",
        "* Java",
        "* Git",
        "# Role",
        "## Basics",
        "Company: Google",
        "Start Date: 01/2020",
        "End Date: 01/2022",
        "Title: Software Engineer",
        "Reason for change: Promoted to Senior software engineer",
        "## Description",
        "Wrote functional program modules",
        "## Responsibilities",
        "This is a paragraph.\nThis is another paragraph.",
        "## Skills",
        "* Python",
        "* Java",
        "* Git",
    ]


def test_parse_role_blocks(resume_markdown, block_lines):
    roles = resume_markdown.parse_work_history_block(block_lines).roles
    assert len(roles) == 2

    assert roles[0].company == "Google"
    assert roles[0].start_date == datetime(2020, 1, 1, 0, 0)
    assert roles[0].end_date == datetime(2022, 1, 1, 0, 0)
    assert roles[0].title == "Senior Software Engineer"
    assert roles[0].reason_for_change == "Promoted to Manager"
    assert (
        roles[0].description
        == "Developed a new feature for the company's flagship product"
    )
    assert (
        roles[0].responsibilities
        == "This is a paragraph.\n\nThis is another paragraph."
    )
    assert roles[0].skills == ["Python", "Java", "Git"]

    assert roles[1].company == "Google"
    assert roles[1].start_date == datetime(2020, 1, 1, 0, 0)
    assert roles[1].end_date == datetime(2022, 1, 1, 0, 0)
    assert roles[1].title == "Software Engineer"
    assert roles[1].reason_for_change == "Promoted to Senior software engineer"
    assert roles[1].description == "Wrote functional program modules"
    assert (
        roles[1].responsibilities == "This is a paragraph.\nThis is another paragraph."
    )
    assert roles[1].skills == ["Python", "Java", "Git"]
