import logging

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from resume_render.render_settings import ResumeCertificationsSettings
from resume_render.resume_render_base import (
    ResumeRenderCertificationBase,
    ResumeRenderCertificationsBase,
)

from resume_writer.models.certifications import Certification, Certifications

log = logging.getLogger(__name__)


class BasicRenderCertificationSection(ResumeRenderCertificationBase):
    """Render Certification Section."""

    def __init__(
        self,
        document: docx.document.Document,
        certification: Certification,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certification renderer."""
        super().__init__(document, certification, settings)

    def render(
        self,
        doc_paragraph: docx.text.paragraph.Paragraph,
    ) -> None:
        """Render the certification section."""
        _paragraph_text = ""

        _certification = self.certification

        if _certification.name and self.settings.name:
            _paragraph_text += f"{_certification.name}\n"

        if _paragraph_text:
            _run = doc_paragraph.add_run(_paragraph_text)
            _run.font.size = Pt(self.font_size - 1)


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

        log.info("Rendering Certifications section.")


        _doc_paragraph = self.document.add_paragraph()
        _doc_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for _certification in self.certifications:
            BasicRenderCertificationSection(
                self.document,
                _certification,
                self.settings,
            ).render(_doc_paragraph)