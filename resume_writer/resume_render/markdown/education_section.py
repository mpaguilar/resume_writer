import logging

from jinja2 import Environment

from resume_writer.models.education import Education
from resume_writer.resume_render.render_settings import ResumeEducationSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderEducationBase,
)
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderEducationSection(ResumeRenderEducationBase):
    """Render Education Section."""

    def __init__(
        self,
        document: MarkdownDoc,
        jinja_env: Environment,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic education renderer."""
        assert isinstance(
            document,
            MarkdownDoc,
        ), f"Expected document to be of type MarkdownDoc, but got {type(document)}"
        assert isinstance(
            jinja_env,
            Environment,
        ), f"Expected jinja_env to be of type Environment, but got {type(jinja_env)}"
        assert isinstance(
            education,
            Education,
        ), f"Expected education to be of type Education, but got {type(education)}"
        assert isinstance(
            settings,
            ResumeEducationSettings,
        ), f"Expected settings to be of type ResumeEducationSettings, but got {type(settings)}"  # noqa: E501

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

