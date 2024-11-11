import logging

from jinja2 import Environment

from resume_writer.models.personal import Personal
from resume_writer.resume_render.render_settings import ResumePersonalSettings
from resume_writer.resume_render.resume_render_text_base import ResumeRenderPersonalBase
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderPersonalSection(ResumeRenderPersonalBase):
    """Render personal contact info section."""

    def __init__(
        self,
        document: MarkdownDoc,
        jinja_env: Environment,
        personal: Personal,
        settings: ResumePersonalSettings,
    ):
        """Initialize the personal section renderer."""

        log.debug("Initializing personal basic render object")

        assert isinstance(
            document,
            MarkdownDoc,
        ), "document must be an instance of MarkdownDoc"
        assert isinstance(
            jinja_env,
            Environment,
        ), "jinja_env must be an instance of Environment"
        assert isinstance(
            personal,
            Personal,
        ), "personal must be an instance of Personal"
        assert isinstance(
            settings,
            ResumePersonalSettings,
        ), "settings must be an instance of ResumePersonalSettings"

        super().__init__(
            document=document,
            jinja_env=jinja_env,
            personal=personal,
            template_name="personal.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render the personal section."""

        # shortcuts
        _doc = self.document
        _personal = self.personal
        _settings = self.settings

        _doc.add_header("# Personal")
        _doc.add_header("## Contact Information")

        if _settings.contact_info and self.personal.contact_info:
            if _settings.name and _personal.contact_info.name:
                _doc.add_text(f"Name: {_personal.contact_info.name}")
            if _settings.email and _personal.contact_info.email:
                _doc.add_text(f"Email: {_personal.contact_info.email}")
            if _settings.phone and _personal.contact_info.phone:
                _doc.add_text(f"Phone: {_personal.contact_info.phone}")
            if _settings.location and _personal.contact_info.location:
                _doc.add_text(f"Location: {_personal.contact_info.location}")

        if _settings.websites and _personal.websites:
            _doc.add_header("## Websites")
            if _settings.github and _personal.websites.github:
                _doc.add_text(f"GitHub: {_personal.websites.github}")
            if _settings.linkedin and _personal.websites.linkedin:
                _doc.add_text(f"LinkedIn: {_personal.websites.linkedin}")
            if _settings.website and _personal.websites.website:
                _doc.add_text(f"Website: {_personal.websites.website}")
            if _settings.twitter and _personal.websites.twitter:
                _doc.add_text(f"Twitter: {_personal.websites.twitter}")

