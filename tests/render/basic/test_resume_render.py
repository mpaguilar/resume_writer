import pytest

from unittest.mock import Mock, MagicMock, patch
import docx.document

from resume_render.basic.basic_personal_section import BasicRenderPersonalSection
from resume_writer.models.resume import Resume
from resume_writer.models.personal import Personal
from resume_writer.models.education import Education
from resume_writer.models.experience import Experience
from resume_writer.models.certifications import Certifications


from resume_writer.resume_render.render_settings import ResumeSettings

from resume_writer.resume_render.basic.basic_resume import BasicRenderResume


@pytest.fixture()
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()


    return _doc


@pytest.fixture()
def settings():
    return ResumeSettings()


@pytest.fixture()
def resume():
    _resume = Mock(spec=Resume)

    _resume.personal = Mock(spec=Personal)
    _resume.education = Mock(spec=Education)
    _resume.experience = Mock(spec=Experience)
    _resume.certifications = Mock(spec=Certifications)
    return _resume


@patch(
    "resume_writer.resume_render.basic.basic_personal_section.BasicRenderPersonalSection.__init__",
    return_value=None,
    spec=BasicRenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.basic.basic_personal_section.BasicRenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_education_section.BasicRenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_education_section.BasicRenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_experience_section.BasicRenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_experience_section.BasicRenderExperienceSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_certifications_section.BasicRenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.basic_certifications_section.BasicRenderCertificationsSection.render",
    return_value=None,
)
def test_render_resume( # noqa: PLR0913

    personal_init, #noqa: ARG001
    personal_render, #noqa: ARG001
    education_init, #noqa: ARG001
    education_render, #noqa: ARG001
    experience_init, #noqa: ARG001
    experience_render, #noqa: ARG001
    certifications_init, #noqa: ARG001
    certifications_render, #noqa: ARG001
    document,
    resume,
    settings,
):
    _resume = BasicRenderResume(document, resume, settings)
    _resume.render()
