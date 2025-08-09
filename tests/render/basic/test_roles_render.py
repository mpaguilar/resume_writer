import pytest
import pytz

import dateparser

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.models.experience import (
    Role,
    Roles,
    RoleSkills,
    RoleBasics,
    RoleSummary,
    RoleResponsibilities,
)
from resume_writer.models.parsers import ParseContext

from resume_writer.resume_render.render_settings import (
    ResumeRolesSettings,
)

from resume_writer.resume_render.basic.experience_section import (
    RenderRoleSection,
    RenderRolesSection,
)


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()

    return _doc


@pytest.fixture
def role():
    role: Role = Mock(spec=Role)
    role.summary = Mock(spec=RoleSummary)
    role.summary.summary = "test summary"

    role.responsibilities = Mock(spec=RoleResponsibilities)
    role.responsibilities.text = "Responsibility 1"

    role.skills = RoleSkills(
        skills=["Skill 1", "Skill 2"],
        parse_context=Mock(spec=ParseContext),
    )

    _basics = Mock(spec=RoleBasics)
    _basics.company = "Company 1"
    _basics.title = "Title 1"
    _basics.location = "Location 1"

    _basics.start_date = dateparser.parse(
        "2020-01-01",
        settings={
            "PREFER_DAY_OF_MONTH": "first",
            "TIMEZONE": "UTC",
        },
    ).astimezone(pytz.utc)

    _basics.end_date = dateparser.parse(
        "2021-01-01",
        settings={
            "PREFER_DAY_OF_MONTH": "first",
            "TO_TIMEZONE": "UTC",
        },
    ).astimezone(pytz.utc)

    _basics.description = "Description 1"

    _basics.job_category = "Job Category 1"
    _basics.agency_name = "Agency Name 1"
    _basics.employment_type = "Employment Type 1"

    role.basics = _basics
    return role


@pytest.fixture
def settings():
    # TODO: does this really need to be mock'd?
    _settings = Mock(spec=ResumeRolesSettings)

    _settings.summary = True
    _settings.skills = True
    _settings.responsibilities = True

    _settings.job_category = True
    _settings.location = True
    _settings.agency_name = True
    _settings.employment_type = True
    _settings.end_date = True
    _settings.start_date = True
    _settings.reason_for_change = True
    _settings.months_ago = 120  # ten years

    return _settings


def test_basic_role_section(document, role, settings):
    section = RenderRoleSection(document=document, role=role, settings=settings)
    section.render()


def test_basic_roles_section(document, role, settings):
    roles = Roles([role], parse_context=Mock(spec=ParseContext))
    section = RenderRolesSection(document=document, roles=roles, settings=settings)
    section.render()


def test_basic_roles_filter(document, role, settings):
    settings.months_ago = 12
    roles = Roles([role], parse_context=Mock(spec=ParseContext))
    section = RenderRolesSection(document=document, roles=roles, settings=settings)
    assert len(section.roles) == 0
    section.render()
