import logging

from jinja2 import Environment

from resume_writer.models.certifications import Certifications
from resume_writer.resume_render.render_settings import ResumeCertificationsSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderCertificationsBase,
)
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderCertificationsSection(ResumeRenderCertificationsBase):
    """Render Certifications Section."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer."""
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            certifications=certifications,
            template_name="certifications.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render the certifications section."""
        if not self.certifications:
            log.debug("No certifications to render.")
            return

        log.debug("Rendering certifications.")

        _rendered = self.template.render(
            settings=self.settings,
            certifications=self.certifications,
        )

        self.document.add_text(_rendered)
