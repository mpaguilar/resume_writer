import pytest
from unittest.mock import Mock, MagicMock, patch
import docx.document

from resume_writer.models.resume import Resume
from resume_writer.models.personal import Personal
from resume_writer.models.education import Education
from resume_writer.models.experience import Experience
from resume_writer.models.certifications import Certifications

from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.plain.personal_section import RenderPersonalSection
from resume_writer.resume_render.plain.resume_main import RenderResume


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()
    _doc.add_heading = MagicMock()
    _doc.add_paragraph = MagicMock()
    _doc.add_page_break = MagicMock()
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
    _resume.parse_context = Mock()
    return _resume


@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.render",
    return_value=None,
)
def test_education_renders_early_when_render_at_end_false(
    experience_render,
    experience_init,  # noqa: ARG001
    skills_matrix_render,
    skills_matrix_init,  # noqa: ARG001
    executive_summary_render,
    executive_summary_init,  # noqa: ARG001
    education_render,
    education_init,  # noqa: ARG001
    certifications_render,
    certifications_init,  # noqa: ARG001
    personal_render,
    personal_init,  # noqa: ARG001
    document,
    resume,
    settings,
):
    """Test Education renders in default position when render_at_end=False."""
    # Setup: render_at_end is False by default
    settings.education_settings.render_at_end = False

    # Enable all sections
    settings.personal = True
    settings.certifications = True
    settings.education = True
    settings.executive_summary = True
    settings.skills_matrix = True
    settings.experience = True

    # Create renderer and render
    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Verify Education.render() was called exactly once
    assert education_render.call_count == 1

    # Verify Experience.render() was also called
    assert experience_render.call_count == 1


@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.render",
    return_value=None,
)
def test_education_renders_at_end_when_render_at_end_true(
    experience_render,
    experience_init,  # noqa: ARG001
    skills_matrix_render,
    skills_matrix_init,  # noqa: ARG001
    executive_summary_render,
    executive_summary_init,  # noqa: ARG001
    education_render,
    education_init,  # noqa: ARG001
    certifications_render,
    certifications_init,  # noqa: ARG001
    personal_render,
    personal_init,  # noqa: ARG001
    document,
    resume,
    settings,
):
    """Test Education renders at end when render_at_end=True."""
    # Setup: render_at_end is True
    settings.education_settings.render_at_end = True

    # Enable all sections
    settings.personal = True
    settings.certifications = True
    settings.education = True
    settings.executive_summary = True
    settings.skills_matrix = True
    settings.experience = True

    # Create renderer and render
    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Verify Education.render() was called exactly once
    assert education_render.call_count == 1

    # Verify Experience.render() was also called
    assert experience_render.call_count == 1


@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.render",
    return_value=None,
)
def test_education_never_renders_twice(
    experience_render,
    experience_init,  # noqa: ARG001
    skills_matrix_render,
    skills_matrix_init,  # noqa: ARG001
    executive_summary_render,
    executive_summary_init,  # noqa: ARG001
    education_render,
    education_init,  # noqa: ARG001
    certifications_render,
    certifications_init,  # noqa: ARG001
    personal_render,
    personal_init,  # noqa: ARG001
    document,
    resume,
    settings,
):
    """Test Education section never renders twice regardless of render_at_end setting."""
    # Test with render_at_end=True
    settings.education_settings.render_at_end = True
    settings.personal = True
    settings.certifications = True
    settings.education = True
    settings.experience = True

    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Should be called exactly once
    assert education_render.call_count == 1

    # Reset mocks
    education_render.reset_mock()

    # Test with render_at_end=False
    settings.education_settings.render_at_end = False

    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Should still be called exactly once
    assert education_render.call_count == 1


@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.render",
    return_value=None,
)
def test_education_not_rendered_when_education_setting_false(
    experience_render,  # noqa: ARG001
    experience_init,  # noqa: ARG001
    skills_matrix_render,  # noqa: ARG001
    skills_matrix_init,  # noqa: ARG001
    executive_summary_render,  # noqa: ARG001
    executive_summary_init,  # noqa: ARG001
    education_render,
    education_init,  # noqa: ARG001
    certifications_render,  # noqa: ARG001
    certifications_init,  # noqa: ARG001
    personal_render,  # noqa: ARG001
    personal_init,  # noqa: ARG001
    document,
    resume,
    settings,
):
    """Test Education not rendered when education setting is False, regardless of render_at_end."""
    # Setup: education disabled but render_at_end=True
    settings.education = False
    settings.education_settings.render_at_end = True
    settings.personal = True
    settings.certifications = True
    settings.experience = True

    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Education should not be rendered
    education_render.assert_not_called()


@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.__init__",
    return_value=None,
    spec=RenderPersonalSection,
)
@patch(
    "resume_writer.resume_render.plain.personal_section.RenderPersonalSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.certifications_section.RenderCertificationsSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.education_section.RenderEducationSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.executive_summary_section.RenderExecutiveSummarySection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.skills_matrix_section.RenderSkillsMatrixSection.render",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.__init__",
    return_value=None,
)
@patch(
    "resume_writer.resume_render.plain.experience_section.RenderExperienceSection.render",
    return_value=None,
)
def test_education_not_rendered_when_no_education_data(
    experience_render,  # noqa: ARG001
    experience_init,  # noqa: ARG001
    skills_matrix_render,  # noqa: ARG001
    skills_matrix_init,  # noqa: ARG001
    executive_summary_render,  # noqa: ARG001
    executive_summary_init,  # noqa: ARG001
    education_render,
    education_init,  # noqa: ARG001
    certifications_render,  # noqa: ARG001
    certifications_init,  # noqa: ARG001
    personal_render,  # noqa: ARG001
    personal_init,  # noqa: ARG001
    document,
    resume,
    settings,
):
    """Test Education not rendered when resume has no education data."""
    # Setup: no education data
    resume.education = None
    settings.education = True
    settings.education_settings.render_at_end = True
    settings.personal = True
    settings.certifications = True
    settings.experience = True

    renderer = RenderResume(document, resume, settings)
    renderer.render()

    # Education should not be rendered
    education_render.assert_not_called()
