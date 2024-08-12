import pytest
from datetime import datetime

from unittest.mock import Mock
import docx.document

from models.resume import Resume
from models.experience import (
    Project,
    Projects,
    ProjectSkills,
    ProjectOverview,
    ProjectDescription,
)

from resume_writer.resume_render.render_settings import (
    ResumeProjectsSettings,
)

from resume_writer.resume_render.basic.basic_experience_section import (
    BasicRenderProjectSection,
    BasicRenderProjectsSection,
)


@pytest.fixture()
def document():
    return Mock(spec=docx.document.Document)


@pytest.fixture()
def resume():
    return Mock(spec=Resume)


@pytest.fixture()
def project():
    project: Project = Mock(spec=Project)
    project.overview = ProjectOverview(
        title="Project Title",
        url="https://example.com",
        url_description="Example Project",
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 12, 31),
    )
    project.skills = ProjectSkills(["Skill 1", "Skill 2"])
    project.description = ProjectDescription("Project 1 description")
    return project


@pytest.fixture()
def settings():
    return ResumeProjectsSettings()


def test_render_project_section(document, project, settings):
    section = BasicRenderProjectSection(document, project, settings)
    section.render()


def test_render_projects_section(document, project, settings):
    section = BasicRenderProjectsSection(document, Projects([project]), settings)
    section.render()
