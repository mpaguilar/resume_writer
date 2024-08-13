import pytest
from datetime import datetime

from unittest.mock import Mock
import docx.document

from resume_writer.models.education import Education, Degree


from resume_writer.resume_render.render_settings import (
    ResumeEducationSettings,
)


from resume_writer.resume_render.basic.basic_education_section import (
    BasicRenderEducationSection,
)


@pytest.fixture()
def document():
    return Mock(spec=docx.document.Document)


@pytest.fixture()
def settings():
    return ResumeEducationSettings()


@pytest.fixture()
def education():
    _degree = Mock(spec=Degree)
    _degree.school = "test school"
    _degree.degree = "test degree"
    _degree.start_date = datetime(2000, 1, 1)
    _degree.end_date = datetime(2004, 1, 1)
    _degree.gpa = 3.5
    _degree.major = "test major"

    return Mock(spec=Education, degrees=[_degree])


def test_render_education_section(document, education, settings):
    section = BasicRenderEducationSection(document, education, settings)
    section.render()
