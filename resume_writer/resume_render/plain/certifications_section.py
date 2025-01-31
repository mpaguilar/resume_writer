import logging

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.resume_render.render_settings import ResumeCertificationsSettings
from resume_writer.resume_render.resume_render_base import (
    ResumeRenderCertificationBase,
    ResumeRenderCertificationsBase,
)

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

    def render(
        self,
        doc_paragraph: docx.text.paragraph.Paragraph,
    ) -> None:
        """Render the certification section.

        Parameters
        ----------
        doc_paragraph : docx.text.paragraph.Paragraph
            The document paragraph to which the certification section will be added.

        Returns
        -------
        None

        Notes
        -----
        1. Initialize an empty string for the paragraph text.
        2. Get the certification object.
        3. If the certification name and settings name are both available,
        append the name to the paragraph text.
        4. If the paragraph text is not empty, add it to the document paragraph
        and adjust the font size.

        """
        _paragraph_text = doc_paragraph.text

        _certification = self.certification

        if _certification.name and self.settings.name:
            _paragraph_text += f"{_certification.name}"

        if _paragraph_text:
            doc_paragraph.text = _paragraph_text
            _run = doc_paragraph.add_run(_paragraph_text)
            _run.font.size = Pt(self.font_size - 1)


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
        """Render the certifications section of a document.

        Parameters
        ----------
        self : object
            The instance of the class containing the method.

        Returns
        -------
        None
            The method does not return any value but modifies the document in-place.

        Notes
        -----
        This method performs the following steps:

        1. Logs an info message indicating the start of rendering the
        Certifications section.
        2. Adds a new paragraph to the document and centers it.
        3. Iterates over each certification in the list of certifications.
        4. For each certification, creates an instance of
        RenderCertificationSection with the document,
        certification, and settings as arguments.
        5. Calls the render method of the RenderCertificationSection instance,
        passing the centered paragraph as an argument.

        """

        log.info("Rendering Certifications section.")

        _doc_paragraph = self.document.add_paragraph()
        _doc_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _doc_paragraph.paragraph_format.space_before = Pt(1)
        _doc_paragraph.paragraph_format.space_after = Pt(1)

        # for a functional resume put everything on one line

        _certification_list = [_cert.name for _cert in self.certifications]

        _doc_paragraph.add_run(" / ".join(_certification_list))

