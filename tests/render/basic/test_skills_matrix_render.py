from datetime import datetime

import pytest

from unittest.mock import Mock, MagicMock, patch
import docx.document
from docx.table import Table, _Rows, _Row

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

from resume_writer.resume_render.render_settings import ResumeSkillsMatrixSettings

from resume_writer.resume_render.basic.skills_matrix_section import (
    RenderSkillsMatrixSection,
)


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()
    _doc.add_table = MagicMock()
    _table = _doc.add_table.return_value = MagicMock(spec=Table)
    _table.rows = MagicMock(spec=_Rows)
    _table.rows.__getitem__.return_value = MagicMock(spec=_Row)

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
    _role.skills.skills = ["test1"]

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
    return Experience(
        roles=roles,
        projects=projects,
    )


@pytest.fixture
def settings():
    _settings = ResumeSkillsMatrixSettings()
    _settings.skills = ["test1", "test2"]
    return _settings


@patch(
    "resume_writer.resume_render.skills_matrix.skills_experience",
    return_value={"test1": 1.0, "test2": 1.0},
)
def test_render_skills_matrix_section(document, experience, settings):
    section = RenderSkillsMatrixSection(document, experience, settings)
    section.render()
