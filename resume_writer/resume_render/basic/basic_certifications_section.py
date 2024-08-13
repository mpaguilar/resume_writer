import logging
from datetime import datetime

import docx.document
from resume_render.render_settings import ResumeCertificationsSettings
from resume_render.resume_render_base import ResumeRenderCertificationsBase

from resume_writer.models.certifications import Certifications

log = logging.getLogger(__name__)


class BasicRenderCertificationsSection(ResumeRenderCertificationsBase):
    """Render Certifications Section."""

    def __init__(
        self,
        document: docx.document.Document,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer."""
        super().__init__(document, certifications, settings)

    def render(self) -> None:
        """Render the certifications section."""

        for _certification in self.certifications:
            _paragraph_lines = []

            if _certification.name and self.settings.name:
                _paragraph_lines.append(f"{_certification.name}")
            if _certification.issuer and self.settings.issuer:
                _paragraph_lines.append(f"{_certification.issuer}")
            if _certification.issued and self.settings.issued:
                _value = datetime.strftime(_certification.issued, "%B %Y")
                _paragraph_lines.append(f"Issued: {_value}")
            if _certification.expires and self.settings.expires:
                _value = datetime.strftime(_certification.expires, "%B %Y")
                _paragraph_lines.append(f"Expires: {_value}")

            if len(_paragraph_lines) > 0:
                _paragraph_text = "\n".join(_paragraph_lines)
                self.document.add_paragraph(_paragraph_text)
