import pytest
from datetime import datetime

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.models.resume import Resume
from resume_writer.models.experience import (
    Project,
    Projects,
    ProjectSkills,
    ProjectOverview,
    ProjectDescription,
)
from resume_writer.models.parsers import ParseContext

from resume_writer.resume_render.render_settings import (
    ResumeProjectsSettings,
)

from resume_writer.resume_render.basic.experience_section import (
    RenderProjectSection,
    RenderProjectsSection,
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
def resume():
    return Mock(spec=Resume)


@pytest.fixture
def project():
    _ctx = Mock(spec=ParseContext)
    project: Project = Mock(spec=Project)
    project.overview = ProjectOverview(
        title="Project Title",
        url="https://example.com",
        url_description="Example Project",
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 12, 31),
        parse_context=_ctx,
    )
    project.skills = ProjectSkills(["Skill 1", "Skill 2"], parse_context=_ctx)
    project.description = ProjectDescription(
        "Project 1 description",
        parse_context=_ctx,
    )
    return project


@pytest.fixture
def settings():
    return ResumeProjectsSettings()


def test_render_project_section(document, project, settings):
    section = RenderProjectSection(document, project, settings)
    section.render()


def test_render_projects_section(document, project, settings):
    section = RenderProjectsSection(
        document,
        Projects([project], parse_context=Mock(spec=ParseContext)),
        settings,
    )
    section.render()
