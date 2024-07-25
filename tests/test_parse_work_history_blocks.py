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


def test_parse_work_history_blocks(resume_markdown, block_lines):
    work_history = resume_markdown.parse_work_history_block(block_lines)
    assert len(work_history) == 2

    assert work_history[0].company == "Google"
    assert work_history[0].start_date == "01/2020"
    assert work_history[0].end_date == "01/2022"
    assert work_history[0].title == "Senior Software Engineer"
    assert work_history[0].reason_for_change == "Promoted to Manager"
    assert (
        work_history[0].description
        == "Developed a new feature for the company's flagship product"
    )
    assert (
        work_history[0].responsibilities
        == "This is a paragraph.\n\nThis is another paragraph."
    )
    assert work_history[0].skills == ["Python", "Java", "Git"]

    assert work_history[1].company == "Google"
    assert work_history[1].start_date == "01/2020"
    assert work_history[1].end_date == "01/2022"
    assert work_history[1].title == "Software Engineer"
    assert work_history[1].reason_for_change == "Promoted to Senior software engineer"
    assert work_history[1].description == "Wrote functional program modules"
    assert (
        work_history[1].responsibilities
        == "This is a paragraph.\nThis is another paragraph."
    )
    assert work_history[1].skills == ["Python", "Java", "Git"]
