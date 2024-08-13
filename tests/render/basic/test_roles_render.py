import pytest
from datetime import datetime

from unittest.mock import Mock
import docx.document

from models.experience import Role, Roles, RoleSkills

from resume_writer.resume_render.render_settings import (
    ResumeRolesSettings,
)

from resume_writer.resume_render.basic.basic_experience_section import (
    BasicRenderRoleSection,
    BasicRenderRolesSection,
)


@pytest.fixture()
def document():
    return Mock(spec=docx.document.Document)


@pytest.fixture()
def role():
    role: Role = Mock(spec=Role)
    role.company = "Company 1"
    role.title = "Title 1"
    role.location = "Location 1"
    role.start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")  # noqa: DTZ007
    role.end_date = datetime.strptime("2021-01-01", "%Y-%m-%d")  # noqa: DTZ007
    role.description = "Description 1"
    role.responsibilities = "Responsibility 1"
    role.job_category = "Job Category 1"
    role.agency_name = "Agency Name 1"
    role.employment_type = "Employment Type 1"
    role.skills = RoleSkills(skills=["Skill 1", "Skill 2"])
    return role


@pytest.fixture()
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

    return _settings


def test_basic_role_section(document, role, settings):
    section = BasicRenderRoleSection(document=document, role=role, settings=settings)
    section.render()


def test_basic_roles_section(document, role, settings):
    roles = Roles([role])
    section = BasicRenderRolesSection(document=document, roles=roles, settings=settings)
    section.render()
