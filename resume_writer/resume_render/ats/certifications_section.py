import logging

import docx.document

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.resume_render.render_settings import ResumeCertificationsSettings
from resume_writer.resume_render.resume_render_base import (
    ResumeRenderCertificationBase,
    ResumeRenderCertificationsBase,
)

log = logging.getLogger(__name__)


class RenderCertificationSection(ResumeRenderCertificationBase):
    """Render Certification Section.

    This class is responsible for rendering a single certification entry in a Word document.
    It uses the provided certification details and settings to format and add the information
    to the document as a formatted paragraph.

    Inherits from:
        ResumeRenderCertificationBase: Base class providing shared functionality for rendering certifications.

    Attributes:
        document (docx.document.Document): The Word document to which the certification will be added.
        certification (Certification): The certification object containing details such as name, issuer, issued date, and expiration date.
        settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display in the rendered output.

    Methods:
        render: Renders the certification details into the document based on enabled settings.
    """

    def __init__(
        self,
        document: docx.document.Document,
        certification: Certification,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certification renderer.

        Args:
            document (docx.document.Document): The Word document to which the certification will be added.
            certification (Certification): The certification object containing details such as name, issuer, issued date, and expiration date.
            settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display in the rendered output.

        Notes:
            1. Calls the parent class constructor to initialize common attributes.

        """
        super().__init__(document, certification, settings)

    def render(self) -> None:
        """Render the certification section in the document.

        This method builds and adds a formatted paragraph for the certification based on enabled settings
        such as showing the name, issuer, issued date, or expiration date.

        Args:
            None: This method does not accept any arguments.

        Returns:
            None: This method does not return any value.

        Notes:
            1. Initializes an empty list to store lines of text for the certification.
            2. If the certification name exists and the name setting is enabled, adds the name to the lines.
            3. If the issuer exists and the issuer setting is enabled, adds the issuer to the lines.
            4. If the issued date exists and the issued setting is enabled, formats the date to "Month Year" and adds it to the lines.
            5. If the expiration date exists and the expires setting is enabled, formats the date to "Month Year" and adds it to the lines.
            6. If any lines were generated, joins them with newline characters and adds the resulting paragraph to the document.

        """
        lines = []

        # Add name if enabled and exists
        if self.certification.name and self.settings.name:
            lines.append(self.certification.name)

        # Add issuer if enabled and exists
        if self.certification.issuer and self.settings.issuer:
            lines.append(self.certification.issuer)

        # Add issued date if enabled and exists
        if self.certification.issued and self.settings.issued:
            lines.append(self.certification.issued.strftime("%B %Y"))

        # Add expiration date if enabled and exists
        if self.certification.expires and self.settings.expires:
            lines.append(self.certification.expires.strftime("%B %Y"))

        # Add the combined text as a paragraph if any content was generated
        if lines:
            paragraph = self.document.add_paragraph("\n".join(lines))
            paragraph.style = "Normal"


class RenderCertificationsSection(ResumeRenderCertificationsBase):
    """Render Certifications Section.

    This class is responsible for rendering the entire certifications section of a resume in a Word document.
    It adds a level-2 heading and then iterates over each certification to render it using the
    RenderCertificationSection class.

    Inherits from:
        ResumeRenderCertificationsBase: Base class providing shared functionality for rendering multiple certifications.

    Attributes:
        document (docx.document.Document): The Word document to which the certifications section will be added.
        certifications (Certifications): A collection of Certification objects to be rendered.
        settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display for each certification.

    Methods:
        render: Renders the entire certifications section with a heading and individual certification entries.
    """

    def __init__(
        self,
        document: docx.document.Document,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer.

        Args:
            document (docx.document.Document): The Word document to which the certifications section will be added.
            certifications (Certifications): A collection of Certification objects to be rendered.
            settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display for each certification.

        Notes:
            1. Calls the parent class constructor to initialize common attributes.

        """
        super().__init__(document, certifications, settings)

    def render(self) -> None:
        """Render the certifications section in the document.

        This method adds a level-2 heading titled "Certifications" and then renders each certification
        in the collection using the RenderCertificationSection class.

        Args:
            None: This method does not accept any arguments.

        Returns:
            None: This method does not return any value.

        Notes:
            1. If there are certifications to render, adds a level-2 heading titled "Certifications".
            2. Iterates through each certification in the collection.
            3. For each certification, creates a RenderCertificationSection instance and renders it into the document.

        """
        if self.certifications:
            heading = self.document.add_heading("Certifications", level=2)
            heading.style = "Heading 2"

            for certification in self.certifications:
                renderer = RenderCertificationSection(self.document, certification, self.settings)
                renderer.render()
