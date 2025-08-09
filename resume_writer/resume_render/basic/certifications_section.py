import logging
from datetime import datetime

import docx.document

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
        """Initialize the basic certification renderer.

        Args:
            document: The Word document object to which the certification will be added.
            certification: The Certification object containing details about the certification.
            settings: The settings object that determines which fields to include in the rendered output.

        Notes:
            1. Calls the parent class constructor to initialize base functionality.
            2. Stores the provided document, certification, and settings as instance attributes.

        """
        super().__init__(document, certification, settings)

    def render(self) -> None:
        """Render the certification section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Initializes an empty list to hold the lines of text to be rendered.
            2. Checks if the certification name exists and the name setting is enabled, and adds it to the lines if so.
            3. Checks if the issuer exists and the issuer setting is enabled, and adds it to the lines if so.
            4. Checks if the issued date exists and the issued setting is enabled, formats it as "Month Year", and adds it to the lines if so.
            5. Checks if the expiration date exists and the expires setting is enabled, formats it as "Month Year", and adds it to the lines if so.
            6. If any lines were collected, joins them with newlines and adds a new paragraph to the document with the resulting text.
            7. No disk, network, or database access occurs during this method.

        """
        _paragraph_lines = []
        _certification = self.certification

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


class RenderCertificationsSection(ResumeRenderCertificationsBase):
    """Render Certifications Section."""

    def __init__(
        self,
        document: docx.document.Document,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer.

        Args:
            document: The Word document object to which the certifications will be added.
            certifications: A list of Certification objects to be rendered.
            settings: The settings object that determines which fields to include in the rendered output.

        Notes:
            1. Calls the parent class constructor to initialize base functionality.
            2. Stores the provided document, certifications, and settings as instance attributes.

        """
        super().__init__(document, certifications, settings)

    def render(self) -> None:
        """Render the certifications section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Checks if there are any certifications to render.
            2. If certifications exist, adds a level-2 heading titled "Certifications" to the document.
            3. Iterates through each certification in the list.
            4. For each certification, creates a new RenderCertificationSection instance and calls its render method to add the certification details to the document.
            5. No disk, network, or database access occurs during this method.

        """
        if len(self.certifications) > 0:
            self.document.add_heading("Certifications", level=2)

        for _certification in self.certifications:
            RenderCertificationSection(
                self.document,
                _certification,
                self.settings,
            ).render()
