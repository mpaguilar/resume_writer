import logging

import docx.document

from resume_writer.models.resume import Resume
from resume_writer.resume_render.basic.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.basic.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.basic.executive_summary_section import (
    RenderExecutiveSummarySection,
)
from resume_writer.resume_render.basic.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.basic.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.basic.skills_matrix_section import (
    RenderSkillsMatrixSection,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.resume_render_base import ResumeRenderBase

log = logging.getLogger(__name__)


class RenderResume(ResumeRenderBase):
    """Render a resume in basic format.

    Attributes:
        document (docx.document.Document): The Word document object to render the resume into.
        resume (Resume): The resume data model containing personal, education, experience, certifications, and other sections.
        settings (ResumeRenderSettings): Configuration settings for rendering specific sections of the resume.

    Args:
        document: The Word document object to render the resume into.
        resume: The resume data model containing personal, education, experience, certifications, and other sections.
        settings: Configuration settings for rendering specific sections of the resume.

    Notes:
        1. The super().__init__() method is called to initialize the base class with the provided document, resume, and settings.
        2. No external file, network, or database access occurs during initialization.
    """

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize basic resume renderer.

        Args:
            document (docx.document.Document): The Word document object to render the resume into.
            resume (Resume): The resume data model containing personal, education, experience, certifications, and other sections.
            settings (ResumeRenderSettings): Configuration settings for rendering specific sections of the resume.

        Notes:
            1. The super().__init__() method is called to initialize the base class with the provided document, resume, and settings.
            2. No external file, network, or database access occurs during initialization.
        """
        super().__init__(document, resume, settings)

    def render(self) -> None:
        """Render the resume by conditionally adding sections based on data and settings.

        Args:
            None: This method does not take any arguments.

        Returns:
            None: This method does not return any value.

        Notes:
            1. Check if the resume has personal information and if the personal section is enabled in settings.
            2. If both conditions are true, render the personal section using RenderPersonalSection.
            3. Check if the resume has education data and if the education section is enabled in settings.
            4. If both conditions are true, render the education section using RenderEducationSection.
            5. Check if the resume has certifications and if the certifications section is enabled in settings.
            6. If both conditions are true, render the certifications section using RenderCertificationsSection.
            7. Check if the resume has experience data and if the executive summary section is enabled in settings.
            8. If both conditions are true, add a heading titled "Executive Summary" and render the summary using RenderExecutiveSummarySection.
            9. Check if the resume has experience data and if the skills matrix section is enabled in settings.
            10. If both conditions are true, render the skills matrix section using RenderSkillsMatrixSection.
            11. Check if the resume has experience data and if the experience section is enabled in settings.
            12. If both conditions are true, render the experience section using RenderExperienceSection.
            13. No external file, network, or database access occurs during rendering.
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
