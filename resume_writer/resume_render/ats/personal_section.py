import logging

import docx.document
from resume_render.render_settings import ResumePersonalSettings
from resume_render.resume_render_base import ResumeRenderPersonalBase

from resume_writer.models.personal import ContactInfo, Personal

log = logging.getLogger(__name__)


class RenderPersonalSection(ResumeRenderPersonalBase):
    """Render personal contact info section."""

    def __init__(
        self,
        document: docx.document.Document,
        personal: Personal,
        settings: ResumePersonalSettings,
    ):
        """Initialize the personal section renderer."""

        log.debug("Initializing personal basic render object")
        super().__init__(document, personal, settings)

    def _contact_info(self) -> None:
        """Render the contact info section."""

        log.debug("Rendering contact info section")

        _paragraph_lines = []

        _info: ContactInfo = self.personal.contact_info
        if _info.name and self.settings.name:
            _paragraph_lines.append(f"{_info.name}")

        if _info.email and self.settings.email:
            _paragraph_lines.append(f"{_info.email}")

        if _info.phone and self.settings.phone:
            _paragraph_lines.append(f"{_info.phone}")

        if _info.location and self.settings.location:
            _paragraph_lines.append(f"{_info.location}")

        if len(_paragraph_lines) > 0:
            self.document.add_paragraph("\n".join(_paragraph_lines))

    def _banner(self) -> None:
        """Render the banner section."""

        log.debug("Rendering banner section")

        _banner = self.personal.banner
        if _banner.text:
            self.document.add_heading("Banner", level=3)
            self.document.add_paragraph(_banner.text)

    def _note(self) -> None:
        """Render the note section."""

        log.debug("Rendering note section")

        _note = self.personal.note
        if _note.text:
            self.document.add_heading("Note", level=3)
            self.document.add_paragraph(_note.text)

    def _websites(self) -> None:
        """Render the websites section."""

        log.debug("Rendering websites section")

        _paragraph_lines = []

        _websites = self.personal.websites

        if _websites.github and self.settings.github:
            _paragraph_lines.append(f"GitHub: {_websites.github}")

        if _websites.linkedin and self.settings.linkedin:
            _paragraph_lines.append(f"LinkedIn: {_websites.linkedin}")

        if _websites.website and self.settings.website:
            _paragraph_lines.append(f"Website: {_websites.website}")

        if _websites.twitter and self.settings.twitter:
            _paragraph_lines.append(f"Twitter: {_websites.twitter}")

        if len(_paragraph_lines) > 0:
            self.document.add_heading("Websites", level=3)
            self.document.add_paragraph("\n".join(_paragraph_lines))

    def _visa_status(self) -> None:
        """Render the visa status section."""

        _paragraph_lines = []

        _visa_status = self.personal.visa_status

        if (
            _visa_status.work_authorization
            and self.settings.work_authorization
        ):
            _paragraph_lines.append(
                f"Work Authorization: {_visa_status.work_authorization}",
            )

        if (
            _visa_status.require_sponsorship is not None
            and self.settings.require_sponsorship
        ):
            _value = "Yes" if _visa_status.require_sponsorship else "No"
            _paragraph_lines.append(f"Require Sponsorship: {_value}")

        if len(_paragraph_lines) > 0:
            self.document.add_heading("Visa Status", level=3)
            self.document.add_paragraph("\n".join(_paragraph_lines))

    def render(self) -> None:
        """Render the personal section."""

        if self.personal.contact_info and self.settings.contact_info:
            self._contact_info()

        if self.personal.banner and self.settings.banner:
            self._banner()

        if self.personal.note and self.settings.note:
            self._note()

        if self.personal.websites and self.settings.websites:
            self._websites()

        if self.personal.visa_status and self.settings.visa_status:
            self._visa_status()
