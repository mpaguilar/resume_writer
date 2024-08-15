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

        _visa_status = self.personal.visa_status
        _work_auth_text = ""

        if _visa_status.work_authorization and self.settings.work_authorization:
            _work_auth_text += f"{_visa_status.work_authorization}"

        if (
            _visa_status.require_sponsorship is not None
            and _visa_status.require_sponsorship
        ):
            _value = "Requires sponsorship"
            if _work_auth_text:
                _work_auth_text += f" | {_value}"

        if _work_auth_text:
            _work_auth_paragraph = self.document.add_paragraph()
            _work_auth_run = _work_auth_paragraph.add_run(_work_auth_text)
            _work_auth_run.font.size = Pt(self.font_size - 2)
            _work_auth_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def render(self) -> None:
        """Render the personal section."""

        if self.document.styles["Normal"].font.size:
            _font_size = self.document.styles["Normal"].font.size.pt
        else:
            raise ValueError("Normal style font size not set.")

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
            _banner_lines.append(self.personal.note.text)

        if len(_contact_lines) > 0:
            _contact_paragraph = self.document.add_paragraph()
            _contact_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _run = _contact_paragraph.add_run("\n".join(_contact_lines))
            _run.font.size = Pt(_font_size - 2)

        if len(_banner_lines) > 0:
            _banner_paragraph = self.document.add_paragraph()

            _txt = "\n".join(_banner_lines)
            _run = _banner_paragraph.add_run(_txt)
            _banner_paragraph.paragraph_format.space_after = Pt(0)
            _banner_paragraph.paragraph_format.space_before = Pt(4)
            _banner_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if self.personal.visa_status and self.settings.visa_status:
            self._visa_status()
