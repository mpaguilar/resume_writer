import logging

from jinja2 import Environment

from resume_writer.models.personal import Personal
from resume_writer.resume_render.render_settings import ResumePersonalSettings
from resume_writer.resume_render.resume_render_text_base import ResumeRenderPersonalBase
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderPersonalSection(ResumeRenderPersonalBase):
    """Render personal contact info section.

    Attributes:
        document (HtmlDoc): The HTML document to which the rendered personal section will be added.
        jinja_env (Environment): The Jinja2 environment used to render the template.
        personal (Personal): The personal information object containing contact details.
        settings (ResumePersonalSettings): The settings object that controls the rendering behavior of the personal section.
    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        personal: Personal,
        settings: ResumePersonalSettings,
    ) -> None:
        """Initialize the personal section renderer.

        Args:
            document (HtmlDoc): The HTML document to which the rendered personal section will be added.
            jinja_env (Environment): The Jinja2 environment used to render the template.
            personal (Personal): The personal information object containing contact details.
            settings (ResumePersonalSettings): The settings object that controls the rendering behavior of the personal section.

        Returns:
            None

        Notes:
            1. Logs a debug message indicating the initialization of the personal section renderer.
            2. Calls the parent class's __init__ method with the provided arguments to set up the base renderer.
        """
        log.debug("Initializing personal basic render object")
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            personal=personal,
            template_name="personal.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render the personal section into the HTML document.

        Args:
            None

        Returns:
            None

        Notes:
            1. Renders the Jinja2 template using the settings and personal data.
            2. Adds the rendered HTML content to the document.
            3. No network, disk, or database access is performed.
        """
        _rendered = self.template.render(settings=self.settings, personal=self.personal)

        self.document.add_text(_rendered)
