import pytest
from datetime import datetime
from unittest.mock import Mock

from resume_model import Role, Resume, Personal, Certification, WorkHistory, Education


@pytest.fixture()
def role_details():
    return {
        "title": "Software Engineer",
        "company": "ABC Inc.",
        "description": "Developed software solutions for various projects.",
        "responsibilities": "Writing enterprise code",
        "skills": ["Python", "Java", "SQL"],
        "reason_for_change": "Seeking new challenges and opportunities.",
    }


@pytest.fixture()
def resume_details():
    return {
        "personal": Mock(spec=Personal),
        "certifications": [Mock(spec=Certification)],
        "work_history": WorkHistory(roles=[]),
        "education": Mock(spec=Education),
    }


def timedelta_to_years(td):
    seconds_per_year = 365.25 * 24 * 60 * 60
    return round(td.total_seconds() / seconds_per_year, 1)


# Tests
def test_years_of_experience(resume_details, role_details):
    resume = Resume(**resume_details)

    # Define the roles using the fixture
    role1 = Role(
        start_date=datetime(2010, 1, 1),
        end_date=datetime(2012, 1, 1),
        **role_details,
    )
    role2 = Role(
        start_date=datetime(2013, 1, 1),
        end_date=datetime(2015, 1, 1),
        **role_details,
    )
    role3 = Role(
        start_date=datetime(2016, 1, 1),
        end_date=datetime(2017, 1, 1),
        **role_details,
    )

    # Set the roles for the resume object
    resume.work_history.roles = [role1, role2, role3]

    # Test with roles having end dates
    assert resume.years_of_experience == 5.0


def test_years_of_experience_no_end_date(resume_details, role_details):
    resume = Resume(**resume_details)

    # Define the roles using the fixture for extra fields
    # two years
    role1 = Role(
        start_date=datetime(2010, 1, 1),
        end_date=datetime(2012, 1, 1),
        **role_details,
    )

    # two years
    role2 = Role(
        start_date=datetime(2013, 1, 1),
        end_date=datetime(2015, 1, 1),
        **role_details,
    )

    # current role, no end date
    role3 = Role(
        start_date=datetime(2016, 1, 1),
        end_date=None,
        **role_details,
    )

    # Set the roles for the resume object
    resume.work_history.roles = [role1, role2, role3]

    # Test with roles having end dates

    _years_at_last_role = timedelta_to_years(datetime.now() - datetime(2016, 1, 1))
    _total_test_years = 2 + 2 + _years_at_last_role

    assert resume.years_of_experience == _total_test_years


def test_years_of_experience_overlapping_roles(resume_details, role_details):
    resume = Resume(**resume_details)

    # two years (2010 - 2012), normal entry
    role1 = Role(
        start_date=datetime(2010, 1, 1),
        end_date=datetime(2012, 1, 1),
        **role_details,
    )

    # skip a year

    # two years, with one year overlap with next role (2013 - 2018)
    # five years
    role2 = Role(
        start_date=datetime(2013, 1, 1),
        end_date=datetime(2015, 1, 1),
        **role_details,
    )

    role3 = Role(
        start_date=datetime(2014, 1, 1),
        end_date=datetime(2018, 1, 1),
        **role_details,
    )

    # start date and end date are within previous role
    # this shouldn't be included in the total
    # zero years
    role4 = Role(
        start_date=datetime(2016, 1, 1),
        end_date=datetime(2017, 1, 1),
        **role_details,
    )

    # Test last role overlaps with previous role
    # should have only two merged entries
    resume.work_history.roles = [role1, role2, role3]
    assert resume.years_of_experience == 7.0

    # Test completely overlapped role, and should not be counted
    # should have only two merged entries
    resume.work_history.roles = [role1, role2, role3, role4]
    assert resume.years_of_experience == 7.0


