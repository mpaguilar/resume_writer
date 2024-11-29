import datetime
from unittest.mock import Mock

import pytest
from resume_writer.models.experience import (
    ParseContext,
    Role,
    Roles,
    RoleBasics,
    RoleSummary,
    RoleResponsibilities,
    RoleSkills,
)
from resume_writer.utils.executive_summary import ExecutiveSummary, Experience


@pytest.fixture
def parse_context():
    return Mock(spec=ParseContext)


@pytest.fixture
def role_basics(parse_context):
    return RoleBasics(
        parse_context=parse_context,
        company="Google",
        start_date="2020-01-01",
        end_date="2021-12-31",
        reason_for_change=None,
        title="Software Engineer",
        location="Mountain View",
        job_category="Software Engineering",
        employment_type="Full-time",
        agency_name=None,
    )


@pytest.fixture
def role_summary(parse_context):
    return RoleSummary(
        "Developed and maintained software applications",
        parse_context=parse_context,
    )


@pytest.fixture
def role_responsibilities(parse_context):
    return RoleResponsibilities(
        parse_context=parse_context,
        text_string="Coding\nTesting\nDebugging",
    )


@pytest.fixture
def role_skills(parse_context):
    return RoleSkills(["Python", "Java", "SQL"], parse_context=parse_context)


@pytest.fixture
def role(parse_context, role_basics, role_summary, role_responsibilities, role_skills):
    return Role(
        parse_context,
        role_basics,
        role_summary,
        role_responsibilities,
        role_skills,
    )


def test_role_initialization(
    parse_context,
    role_basics,
    role_summary,
    role_responsibilities,
    role_skills,
):
    role = Role(
        parse_context=parse_context,
        basics=role_basics,
        summary=role_summary,
        responsibilities=role_responsibilities,
        skills=role_skills,
    )
    assert role.basics == role_basics
    assert role.summary == role_summary
    assert role.responsibilities == role_responsibilities
    assert role.skills == role_skills
    assert role.parse_context == parse_context


def test_role_initialization_invalid_types(parse_context):
    with pytest.raises(AssertionError):
        Role("invalid", None, None, None, None)
    with pytest.raises(AssertionError):
        Role(parse_context, "invalid", None, None, None)
    with pytest.raises(AssertionError):
        Role(parse_context, None, "invalid", None, None)
    with pytest.raises(AssertionError):
        Role(parse_context, None, None, "invalid", None)
    with pytest.raises(AssertionError):
        Role(parse_context, None, None, None, "invalid")


@pytest.fixture
def experience(role, parse_context):
    return Experience(
        parse_context=parse_context,
        roles=Roles([role], parse_context=parse_context),
        projects=None,
    )


def test_executive_summary_initialization(experience):
    summary = ExecutiveSummary(
        experience=experience,
    )
    assert summary.experience == experience

@pytest.fixture
def executive_summary(experience):
    return ExecutiveSummary(experience)

def test_executive_summary_available_categories(executive_summary):
    _categories = executive_summary.available_categories()
    assert len(_categories) == 1
    assert "Software Engineering" in _categories


def test_executive_summary_summary(executive_summary):
    summaries = executive_summary.summary(["Software Engineering"])

    _swe_summary = summaries["Software Engineering"]

    assert len(_swe_summary) == 1
    _swe_summary = _swe_summary[0]
    assert "summary" in _swe_summary
    assert "company" in _swe_summary
    assert "first_date" in _swe_summary
    assert "last_date" in _swe_summary
    assert "title" in _swe_summary

    assert _swe_summary["summary"] == "Developed and maintained software applications"
    assert _swe_summary["company"] == "Google"
    assert _swe_summary["title"] == "Software Engineer"
    assert datetime.datetime(2020, 1, 1, 0, 0) == _swe_summary["first_date"]
    assert datetime.datetime(2021, 12, 31, 0, 0) == _swe_summary["last_date"]


def test_executive_summary_summary_empty_category(executive_summary):
    summaries = executive_summary.summary(["Product Management"])
    assert "Product Management" not in summaries

