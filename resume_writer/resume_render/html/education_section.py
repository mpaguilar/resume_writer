import logging

from jinja2 import Environment

from resume_writer.models.education import Education
from resume_writer.resume_render.render_settings import ResumeEducationSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderEducationBase,
)
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)

class RenderEducationSection(ResumeRenderEducationBase):
    """Render Education Section."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic education renderer."""
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            education=education,
            template_name="education.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render the education section."""

        if not self.settings.degrees:
            log.debug("No degrees to render.")
            return

        log.debug("Rendering education section.")

        _rendered = self.template.render(
            settings=self.settings, education=self.education,
        )

        self.document.add_text(_rendered)
