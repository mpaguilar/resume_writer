import logging

from jinja2 import Environment

from resume_writer.models.resume import Resume
from resume_writer.resume_render.html.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.html.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.html.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.html.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderBase,
)
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderResume(ResumeRenderBase):
    """Render a resume in HTML format.

    Attributes:
        document (HtmlDoc): The HTML document to render into.
        jinja_env (Environment): The Jinja2 environment used for templating.
        resume (Resume): The resume data to render.
        settings (ResumeRenderSettings): The rendering settings for the resume.

    Inherits from:
        ResumeRenderBase: Base class for rendering resume sections.
    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize the HTML resume renderer.

        Args:
            document (HtmlDoc): The HTML document to render into.
            jinja_env (Environment): The Jinja2 environment used for templating.
            resume (Resume): The resume data to render.
            settings (ResumeRenderSettings): The rendering settings for the resume.

        Notes:
            1. Calls the parent constructor with the provided arguments.
        """
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            resume=resume,
            settings=settings,
        )

    def render(self) -> None:
        """Render the resume by processing each section.

        Args:
            None

        Returns:
            None: This function does not return a value.

        Notes:
            1. If the resume has personal information and personal rendering is enabled, render the personal section.
            2. If the resume has education data and education rendering is enabled, render the education section.
            3. If the resume has certifications and certifications rendering is enabled, render the certifications section.
            4. If the resume has experience data and experience rendering is enabled, render the experience section.
            5. No disk, network, or database access occurs during this process.
        """
        if self.resume.personal and self.settings.personal:
            RenderPersonalSection(
                document=self.document,
                personal=self.resume.personal,
                jinja_env=self.jinja_env,
                settings=self.settings.personal_settings,
            ).render()

        if self.resume.education and self.settings.education:
            RenderEducationSection(
                document=self.document,
                jinja_env=self.jinja_env,
                education=self.resume.education,
                settings=self.settings.education_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            RenderCertificationsSection(
                document=self.document,
                jinja_env=self.jinja_env,
                certifications=self.resume.certifications,
                settings=self.settings.certifications_settings,
            ).render()

        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                document=self.document,
                jinja_env=self.jinja_env,
                experience=self.resume.experience,
                settings=self.settings.experience_settings,
            ).render()
