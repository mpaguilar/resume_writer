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
        """Initialize basic resume renderer.

        Args:
            document (docx.document.Document): The Word document object to render into.
            resume (Resume): The parsed resume data structure containing personal, education, experience, certifications, and other sections.
            settings (ResumeRenderSettings): Configuration settings for rendering, including which sections to render and their formatting options.

        Returns:
            None

        Notes:
            1. Stores the provided document, resume, and settings as instance attributes.
            2. Initializes the base class ResumeRenderBase with the provided document, resume, and settings.
            3. No external disk, network, or database access occurs during initialization.

        """
        self.parse_context = resume.parse_context
        super().__init__(document, resume, settings)

    def render(self) -> None:
        """Render the resume by sequentially rendering each enabled section.

        Args:
            None

        Returns:
            None

        Notes:
            1. If personal information is present in the resume and personal section rendering is enabled, render the personal section.
            2. If certifications are present and certification section rendering is enabled, render the certifications section.
            3. If education data exists and education section rendering is enabled, render the education section.
            4. If experience data exists and executive summary rendering is enabled, add a centered heading "Executive Summary", then render the executive summary section using experience data.
            5. If experience data exists and skills matrix rendering is enabled (but not necessarily executive summary), render the skills matrix section using experience data.
            6. If both experience and executive summary rendering are enabled, insert a page break after the executive summary.
            7. If experience data exists and experience section rendering is enabled, render the full experience section.
            8. No external disk, network, or database access occurs during rendering.

        """
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
            self.resume.experience and self.settings.skills_matrix
            # and self.settings.executive_summary
        ):
            # add a blank line
            self.document.add_paragraph()
            RenderSkillsMatrixSection(
                document=self.document,
                experience=self.resume.experience,
                settings=self.settings.skills_matrix_settings,
                parse_context=self.parse_context,
            ).render()

        # don't add a page break if we're rendering only the summary
        if self.settings.experience and self.settings.executive_summary:
            self.document.add_page_break()

        # render all the roles
        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
