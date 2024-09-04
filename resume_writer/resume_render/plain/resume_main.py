import logging

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from resume_writer.models.resume import Resume
from resume_writer.resume_render.plain.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.plain.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.plain.executive_summary_section import (
    RenderExecutiveSummarySection,
)
from resume_writer.resume_render.plain.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.plain.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.plain.skills_matrix_section import (
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
        """Initialize basic resume renderer."""
        super().__init__(document, resume, settings)

    def render(self) -> None:
        """Render the resume."""

        if self.resume.personal and self.settings.personal:
            RenderPersonalSection(
                self.document,
                self.resume.personal,
                self.settings.personal_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            RenderCertificationsSection(
                self.document,
                self.resume.certifications,
                self.settings.certifications_settings,
            ).render()

        if self.resume.education and self.settings.education:
            RenderEducationSection(
                self.document,
                self.resume.education,
                self.settings.education_settings,
            ).render()

        # the executive summary is built from experience, so it has to exist
        if self.resume.experience and self.settings.executive_summary:
            _heading = self.document.add_heading("Executive Summary", 2)
            _heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

            RenderExecutiveSummarySection(
                self.document,
                self.resume.experience,
                self.settings.executive_summary_settings,
            ).render()

        # the skills section is built from experience, so it has to exist
        # Only render the skills matrix if we have an executive summary
        if (
            self.resume.experience
            and self.settings.skills_matrix
            and self.settings.executive_summary
        ):
            # add a blank line
            self.document.add_paragraph()
            RenderSkillsMatrixSection(
                self.document,
                self.resume.experience,
                self.settings.skills_matrix_settings,
            ).render()

            self.document.add_page_break()

        # render all the roles
        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
