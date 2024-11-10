import logging

from jinja2 import Environment

from resume_writer.models.personal import Personal
from resume_writer.resume_render.render_settings import ResumePersonalSettings
from resume_writer.resume_render.resume_render_text_base import ResumeRenderPersonalBase
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderPersonalSection(ResumeRenderPersonalBase):
    """Render personal contact info section."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        personal: Personal,
        settings: ResumePersonalSettings,
    ):
        """Initialize the personal section renderer."""

        log.debug("Initializing personal basic render object")
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            personal=personal,
            template_name="personal.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render the personal section."""

        _rendered = self.template.render(settings=self.settings, personal=self.personal)

        self.document.add_text(_rendered)

