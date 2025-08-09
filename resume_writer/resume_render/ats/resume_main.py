import logging

import docx.document

from resume_writer.models.resume import Resume
from resume_writer.resume_render.ats.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.ats.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.ats.executive_summary_section import (
    RenderExecutiveSummarySection,
)
from resume_writer.resume_render.ats.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.ats.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.ats.skills_matrix_section import (
    RenderSkillsMatrixSection,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.resume_render_base import ResumeRenderBase

log = logging.getLogger(__name__)


class RenderResume(ResumeRenderBase):
    """Render a resume in basic format."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize ATS resume renderer.

        Args:
            document: The Word document object to render the resume into.
            resume: The parsed resume data structure containing personal, education,
                    experience, certifications, and other sections.
            settings: Configuration settings for rendering the resume, including
                      which sections to include and how they should be formatted.

        Notes:
            1. Calls the parent class constructor to initialize common rendering state.
            2. Applies default settings overrides specific to ATS resume formatting.

        """
        super().__init__(document, resume, settings)
        self._settings_override()

    def _settings_override(self) -> None:
        """Apply default settings overrides for ATS resumes.

        Args:
            None

        Returns:
            None

        Notes:
            1. Disables the inclusion of role summaries in the experience section.
            2. Disables the executive summary section.
            3. Disables the skills matrix section.
            4. These settings are enforced to ensure compatibility with applicant tracking systems.

        """
        self.settings.experience_settings.roles_settings.summary = False
        self.settings.executive_summary = False
        self.settings.skills_matrix = False

    def render(self) -> None:
        """Render the resume by processing each enabled section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Checks if personal information exists and the personal section is enabled.
            2. If enabled, renders the personal section using RenderPersonalSection.
            3. Checks if education data exists and the education section is enabled.
            4. If enabled, renders the education section using RenderEducationSection.
            5. Checks if certifications exist and the certifications section is enabled.
            6. If enabled, renders the certifications section using RenderCertificationsSection.
            7. Checks if experience data exists and the executive summary is enabled.
            8. If enabled, adds a heading "Executive Summary" and renders the summary using RenderExecutiveSummarySection.
            9. Checks if experience data exists and the skills matrix is enabled.
            10. If enabled, renders the skills matrix using RenderSkillsMatrixSection.
            11. Checks if experience data exists and the experience section is enabled.
            12. If enabled, renders the experience section using RenderExperienceSection.

        """
        if self.resume.personal and self.settings.personal:
            RenderPersonalSection(
                self.document,
                self.resume.personal,
                self.settings.personal_settings,
            ).render()

        if self.resume.education and self.settings.education:
            RenderEducationSection(
                self.document,
                self.resume.education,
                self.settings.education_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            RenderCertificationsSection(
                self.document,
                self.resume.certifications,
                self.settings.certifications_settings,
            ).render()

        # the executive summary is built from experience, so it has to exist
        if self.resume.experience and self.settings.executive_summary:
            self.document.add_heading("Executive Summary", 2)

            RenderExecutiveSummarySection(
                self.document,
                self.resume.experience,
                self.settings.executive_summary_settings,
            ).render()

        # the skills section is built from experience, so it has to exist
        if self.resume.experience and self.settings.skills_matrix:
            RenderSkillsMatrixSection(
                self.document,
                self.resume.experience,
                self.settings.skills_matrix_settings,
            ).render()

        # render all the roles
        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
