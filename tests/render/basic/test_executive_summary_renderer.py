from datetime import datetime

import pytest

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.models.experience import (
    Experience,
    ProjectDescription,
    ProjectOverview,
    ProjectSkills,
    Roles,
    RoleBasics,
    RoleSummary,
    RoleSkills,
    RoleResponsibilities,
    Projects,
    Project,
    Role,
)

from resume_writer.resume_render.render_settings import ResumeExecutiveSummarySettings
from resume_writer.models.parsers import ParseContext

from resume_writer.resume_render.basic.executive_summary_section import (
    RenderExecutiveSummarySection,
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
    _role = Mock(spec=Role)

    _role.basics = Mock(spec=RoleBasics)
    _role.basics.company = "test"
    _role.basics.start_date = datetime.strptime("01/2020", "%m/%Y")  # noqa: DTZ007
    _role.basics.end_date = datetime.strptime("01/2021", "%m/%Y")  # noqa: DTZ007
    _role.basics.title = "test"
    _role.basics.location = "test"
    _role.basics.job_category = "test"
    _role.basics.employment_type = "test"
    _role.basics.agency_name = "test"

    _role.summary = Mock(spec=RoleSummary)
    _role.summary.summary = "test"

    _role.responsibilities = Mock(spec=RoleResponsibilities)
    _role.responsibilities.text = "test"

    _role.skills = MagicMock(spec=RoleSkills)
    _role.skills.skills = ["test"]

    return _role


@pytest.fixture
def roles(role):
    _roles = MagicMock(spec=Roles)
    _roles.roles = [role]
    _roles.__len__.return_value = 1
    _roles.__iter__.return_value = iter(_roles.roles)

    return _roles


@pytest.fixture
def project():
    _project = Mock(spec=Project)
    _project.overview = Mock(spec=ProjectOverview)
    _project.overview.title = "test"
    _project.overview.url = "test"
    _project.overview.url_description = "test"
    _project.overview.start_date = datetime.strptime("01/2020", "%m/%Y")  # noqa: DTZ007
    _project.overview.end_date = datetime.strptime("01/2021", "%m/%Y")  # noqa: DTZ007

    _project.description = Mock(spec=ProjectDescription)
    _project.description.text = "test"

    _project.skills = MagicMock(spec=ProjectSkills)
    return _project


@pytest.fixture
def projects(project):
    _projects = Mock(spec=Projects)
    _projects.__len__ = Mock()
    _projects.__len__.return_value = 1

    _projects.projects = [project]
    _projects.__iter__ = Mock()
    _projects.__iter__.return_value = iter(_projects.projects)
    return _projects


@pytest.fixture
def experience(projects, roles):
    _ctx = Mock(spec=ParseContext)
    return Experience(
        roles=roles,
        projects=projects,
        parse_context=_ctx,
    )


@pytest.fixture
def settings():
    _settings = ResumeExecutiveSummarySettings()
    _settings.categories = ["test1", "test2"]
    return _settings


def test_render_executive_summary_section(document, experience, settings):
    section = RenderExecutiveSummarySection(document, experience, settings)
    section.render()
