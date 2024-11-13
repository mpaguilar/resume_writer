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
    """Render a resume in basic format."""

    def __init__(
        self,
        document: MarkdownDoc,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize basic resume renderer."""
        super().__init__(
            document=document,
            resume=resume,
            settings=settings,
            jinja_env=None,
        )

    def render(self) -> None:
        """Render the resume."""

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

