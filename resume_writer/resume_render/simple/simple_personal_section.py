import logging

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from resume_render.render_settings import ResumePersonalSettings
from resume_render.resume_render_base import ResumeRenderPersonalBase

from resume_writer.models.personal import ContactInfo, Personal

log = logging.getLogger(__name__)


class BasicRenderPersonalSection(ResumeRenderPersonalBase):
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

    def _contact_info(self) -> str | None:
        """Render the contact info section."""

        log.debug("Rendering contact info section")

        _info: ContactInfo = self.personal.contact_info
        if _info.name and self.settings.name:
            _heading = self.document.add_heading(_info.name, level=1)
            _heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        _contact_line = ""

        if _info.email and self.settings.email:
            _contact_line += f"{_info.email}"

        if _info.phone and self.settings.phone:
            _contact_line += f" | {_info.phone}"

        if _info.location and self.settings.location:
            _contact_line += f" | {_info.location}"

        if _contact_line:
            return _contact_line
        return None

    def _websites(self) -> str | None:
        """Render the websites section."""

        # TODO: This runs over one line if all the sites are populated

        log.debug("Rendering websites section")

        _websites = self.personal.websites

        _paragraph_text = ""
        _doc_runs = []

        if _websites.github and self.settings.github:
            _doc_runs.append(f"{_websites.github}")
            _paragraph_text += f"{_websites.github}"

        if _websites.linkedin and self.settings.linkedin:
            _paragraph_text += f" | {_websites.linkedin}"

        if _websites.website and self.settings.website:
            _paragraph_text += f" | {_websites.website}"

        if _websites.twitter and self.settings.twitter:
            _paragraph_text += f" | {_websites.twitter}"

        if _paragraph_text:
            return _paragraph_text

        return None

    def _visa_status(self) -> None:
        """Render the visa status section."""

        _paragraph_lines = []

        _visa_status = self.personal.visa_status

        if _visa_status.work_authorization and self.settings.work_authorization:
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

        _font_size = 9

        log.debug("Rendering personal section")
        _contact_lines = []
        _banner_lines = []

        if self.personal.contact_info and self.settings.contact_info:
            _contact_lines.append(self._contact_info())

        if self.personal.websites and self.settings.websites:
            _contact_lines.append(self._websites())

        if self.personal.banner and self.settings.banner and self.personal.banner.text:
            _banner_lines.append(self.personal.banner.text)

        if self.personal.note and self.settings.note and self.personal.note.text:
            _note = self.personal.note.text
            _banner_lines.append(self.personal.note.text)

        _paragraph = None
        if len(_banner_lines) > 0 or len(_contact_lines) > 0:
            _paragraph = self.document.add_paragraph()
            _paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if len(_contact_lines) > 0:
            _run = _paragraph.add_run("\n".join(_contact_lines))
            _run.font.size = Pt(_font_size - 1)

        if len(_banner_lines) > 0:
            _txt = "\n\n" if len(_contact_lines) > 0 else ""
            _txt = _txt + "\n".join(_banner_lines)
            _run = _paragraph.add_run(_txt)
            _run.font.size = Pt(_font_size)

        if self.personal.visa_status and self.settings.visa_status:
            self._visa_status()
