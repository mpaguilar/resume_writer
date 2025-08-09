import logging

from resume_writer.models.resume import Resume
from resume_writer.resume_render.markdown.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.markdown.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.markdown.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.markdown.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderBase,
)
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderResume(ResumeRenderBase):
    """Render a resume in basic Markdown format.

    Attributes:
        document (MarkdownDoc): The Markdown document to render the resume into.
        resume (Resume): The resume data to render.
        settings (ResumeRenderSettings): The rendering settings for the resume.
    """

    def __init__(
        self,
        document: MarkdownDoc,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize the basic resume renderer.

        Args:
            document (MarkdownDoc): The Markdown document to render the resume into.
            resume (Resume): The resume data to render.
            settings (ResumeRenderSettings): The rendering settings for the resume.

        Returns:
            None: This method does not return anything.

        Notes:
            1. Calls the parent class constructor to initialize the base renderer.
            2. Stores the provided document, resume, and settings for later use during rendering.

        """
        super().__init__(
            document=document,
            resume=resume,
            settings=settings,
            jinja_env=None,
        )

    def render(self) -> None:
        """Render the resume by generating sections based on provided data and settings.

        Args:
            None: This method does not take any arguments.

        Returns:
            None: This method does not return anything.

        Notes:
            1. Checks if the resume has personal information and if personal section rendering is enabled.
            2. If both conditions are true, renders the personal section.
            3. Checks if the resume has education information and if education section rendering is enabled.
            4. If both conditions are true, renders the education section.
            5. Checks if the resume has certifications and if certifications section rendering is enabled.
            6. If both conditions are true, renders the certifications section.
            7. Checks if the resume has experience information and if experience section rendering is enabled.
            8. If both conditions are true, renders the experience section.
            9. This method performs no disk, network, or database access.

        """
        if self.resume.personal and self.settings.personal:
            RenderPersonalSection(
                document=self.document,
                personal=self.resume.personal,
                settings=self.settings.personal_settings,
            ).render()

        if self.resume.education and self.settings.education:
            RenderEducationSection(
                document=self.document,
                education=self.resume.education,
                settings=self.settings.education_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            RenderCertificationsSection(
                document=self.document,
                certifications=self.resume.certifications,
                settings=self.settings.certifications_settings,
            ).render()

        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                document=self.document,
                experience=self.resume.experience,
                settings=self.settings.experience_settings,
            ).render()
