from datetime import datetime

import pytest
from unittest.mock import mock_open, patch
from resume_model import Education
from resume_writer.resume_markdown import (
    MarkdownResumeParser,
    
    Degree,
    WorkHistory,
    Role,
    Certification,
)


@pytest.fixture()
def mock_file_content():
    return """
# Personal

## Info
name: John Doe
email: johndoe@example.com
phone: 123-456-7890

## Banner

Experienced Widget Expert with a lot of experience in the field.

## Note

Proficent in the skills employers look for.

# Education

## Degree
School: University of Example
Degree: Impressive Degree
Started: 08/1990
Ended: 05/1994

## Degree
School: University of College
Degree: Less Impressive Degree
Started: 08/1986
Ended: 05/1989

# Certifications

## Certification

Issuer: BigCorp
Name: BigCorp Certified Widget Expert
Issued: 03/2020

## Certification
Issuer: BigCorp
Name: BigCorp Certified Thing Expert
Issued: 04/2020

# Work history

## Role

### Basics
Company: Another Company
Start date: 01/2023
End date: 01/2024
Title: Senior Worker

Reason for change: Searching for new opportunities

### Description
Performed senior tasks

### Responsibilities
Performed activities associated with a senior role.

### Skills
* Skill 1
* Skill 2
* Skill 3

## Role

### Basics
Company: Example Company

Start date: 06/2020

End date: 06/2022

Title: Junior Worker

Reason for change: Laid off

### Description
Performed junior tasks.

### Responsibilities
Performed routine activities associated with a junor role.

### Skills

* Skill 1
* Skill 2
* Skill 4

"""


def test_parse_personal(mock_file_content):
    resume_lines = mock_file_content.split("\n")
    # Extract the personal section from the mock file content
    personal_lines = "\n".join(resume_lines[:15])


def test_parse_education(mock_file_content):
    resume_lines = mock_file_content.split("\n")
    # Extract the education section from the mock file content
    education_lines = "\n".join(resume_lines[16:28])

    with patch("builtins.open", mock_open(read_data=education_lines)):
        _resume_parser = MarkdownResumeParser("fake_path.md")
        resume = _resume_parser.parse()
        education = resume.education

    assert isinstance(education, Education)
    assert len(education.degrees) == 2
    assert isinstance(education.degrees[0], Degree)
    assert education.degrees[0].school == "University of Example"
    assert education.degrees[0].degree == "Impressive Degree"
    assert education.degrees[0].start_date == datetime(1990, 8, 1, 0, 0)
    assert education.degrees[0].end_date == datetime(1994, 5, 1, 0, 0)


def test_parse_work_history(mock_file_content):
    resume_lines = mock_file_content.split("\n")
    # Extract the work history section from the mock file content
    work_history_lines = "\n".join(resume_lines[30:])
    with patch("builtins.open", mock_open(read_data=work_history_lines)):
        _resume_parser = MarkdownResumeParser("fake_path.md")
        resume = _resume_parser.parse()
        work_history = resume.work_history

    assert isinstance(work_history, WorkHistory)
    # Two roles
    assert len(work_history.roles) == 2
    # First role
    assert isinstance(work_history.roles[0], Role)
    assert work_history.roles[0].company == "Another Company"
    assert work_history.roles[0].title == "Senior Worker"
    assert work_history.roles[0].start_date == datetime(2023, 1, 1, 0, 0)
    assert work_history.roles[0].end_date == datetime(2024, 1, 1, 0, 0)
    # Three skills
    assert len(work_history.roles[0].skills) == 3
    assert "Skill 1" in work_history.roles[0].skills
    assert "Skill 2" in work_history.roles[0].skills
    assert "Skill 3" in work_history.roles[0].skills
    # Second role
    assert isinstance(work_history.roles[1], Role)
    assert work_history.roles[1].company == "Example Company"
    assert work_history.roles[1].title == "Junior Worker"
    assert work_history.roles[1].start_date == datetime(2020, 6, 1, 0, 0)
    assert work_history.roles[1].end_date == datetime(2022, 6, 1, 0, 0)
    # Three skills, one different than before
    assert len(work_history.roles[1].skills) == 3
    assert "Skill 1" in work_history.roles[1].skills
    assert "Skill 2" in work_history.roles[1].skills
    assert "Skill 4" in work_history.roles[1].skills


def test_parse_certifications(mock_file_content):
    resume_lines = mock_file_content.split("\n")
    # Extract the certifications section from the mock file content
    certifications_lines = "\n".join(resume_lines[30:42])
    with patch("builtins.open", mock_open(read_data=certifications_lines)):
        _resume_parser = MarkdownResumeParser("fake_path.md")
        resume = _resume_parser.parse()
        certifications = resume.certifications

        assert isinstance(certifications, list)
        assert len(certifications) == 2
        assert isinstance(certifications[0], Certification)


def test_overall_stats(mock_file_content):
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        _resume_parser = MarkdownResumeParser("fake_path.md")
        resume = _resume_parser.parse()
        overall_stats = resume.stats()

        assert isinstance(overall_stats, dict)
        assert "education" in overall_stats
        assert overall_stats["education"] == 2

        assert "roles" in overall_stats
        assert overall_stats["roles"] == 2

        assert "certifications" in overall_stats
        assert overall_stats["certifications"] == 2

        assert "total_experience" in overall_stats
        assert overall_stats["total_experience"] == 3.0

        assert "career_experience" in overall_stats
        assert overall_stats["career_experience"] == 3.6
