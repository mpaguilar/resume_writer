import pytest

from unittest.mock import Mock, MagicMock, patch
import docx.document

from resume_writer.resume_render.basic.personal_section import RenderPersonalSection
from resume_writer.models.resume import Resume
from resume_writer.models.personal import Personal
from resume_writer.models.education import Education
from resume_writer.models.experience import Experience
from resume_writer.models.certifications import Certifications


from resume_writer.resume_render.render_settings import ResumeRenderSettings

from resume_writer.resume_render.basic.resume_main import RenderResume


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()

    return _doc


@pytest.fixture
def settings():
    return ResumeRenderSettings()


@pytest.fixture
def resume():
    _resume = Mock(spec=Resume)

    _resume.personal = Mock(spec=Personal)
    _resume.education = Mock(spec=Education)
    _resume.experience = Mock(spec=Experience)
    _resume.certifications = Mock(spec=Certifications)
    return _resume


@patch(
    "resume_writer.resume_render.basic.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.basic.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.experience_section.RenderExperienceSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.basic.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
def test_render_resume(  # noqa: PLR0913
    personal_init,  # noqa: ARG001
    personal_render,  # noqa: ARG001
    education_init,  # noqa: ARG001
    education_render,  # noqa: ARG001
    experience_init,  # noqa: ARG001
    experience_render,  # noqa: ARG001
    executive_summary_experience_init,  # noqa: ARG001
    executive_summary_experience_render,  # noqa: ARG001
    skills_matrix_render,  # noqa: ARG001
    skills_matrix_init,  # noqa: ARG001
    certifications_init,  # noqa: ARG001
    certifications_render,  # noqa: ARG001
    document,
    resume,
    settings,
):
    _resume = RenderResume(document, resume, settings)
    _resume.render()
