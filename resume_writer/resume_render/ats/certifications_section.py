import logging
from datetime import datetime

import docx.document
from resume_render.render_settings import ResumeCertificationsSettings
from resume_render.resume_render_base import (
    ResumeRenderCertificationBase,
    ResumeRenderCertificationsBase,
)

from resume_writer.models.certifications import Certification, Certifications

log = logging.getLogger(__name__)


class RenderCertificationSection(ResumeRenderCertificationBase):
    """Render Certification Section."""

    def __init__(
        self,
        document: docx.document.Document,
        certification: Certification,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certification renderer."""
        super().__init__(document, certification, settings)

    def render(self) -> None:
        """Render the certification section."""
        _paragraph_lines = []
        _certification = self.certification

        if _certification.name and self.settings.name:
            _paragraph_lines.append(f"{_certification.name}")
        if _certification.issuer and self.settings.issuer:
            _paragraph_lines.append(f"Issued by: {_certification.issuer}")
        if _certification.issued and self.settings.issued:
            _value = datetime.strftime(_certification.issued, "%B %Y")
            _paragraph_lines.append(f"Issued: {_value}")
        if _certification.expires and self.settings.expires:
            _value = datetime.strftime(_certification.expires, "%B %Y")
            _paragraph_lines.append(f"Expires: {_value}")

        if len(_paragraph_lines) > 0:
            _paragraph_text = "\n".join(_paragraph_lines)
            self.document.add_paragraph(_paragraph_text)


class RenderCertificationsSection(ResumeRenderCertificationsBase):
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

        if len(self.certifications) > 0:
            self.document.add_heading("Certifications", level=3)

        for _certification in self.certifications:
            RenderCertificationSection(
                self.document,
                _certification,
                self.settings,
            ).render()
