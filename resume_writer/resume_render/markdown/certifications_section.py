import logging

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.resume_render.render_settings import ResumeCertificationsSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderCertificationsBase,
)
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderCertificationsSection(ResumeRenderCertificationsBase):
    """Render Certifications Section."""

    def __init__(
        self,
        document: MarkdownDoc,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer.

        Args:
            document: The MarkdownDoc instance to which the rendered content will be added.
            certifications: The Certifications object containing the list of certifications to render.
            settings: The ResumeCertificationsSettings object that controls what information to include in the output.

        Returns:
            None

        Notes:
            1. Validate that the document is an instance of MarkdownDoc.
            2. Validate that the certifications is an instance of Certifications.
            3. Validate that the settings is an instance of ResumeCertificationsSettings.
            4. Call the parent class constructor with the provided arguments.

        """
        assert isinstance(
            document,
            MarkdownDoc,
        ), "document must be an instance of MarkdownDoc"
        assert isinstance(
            certifications,
            Certifications,
        ), "certifications must be an instance of Certifications"
        assert isinstance(
            settings,
            ResumeCertificationsSettings,
        ), "settings must be an instance of ResumeCertificationsSettings"

        super().__init__(
            document=document,
            certifications=certifications,
            template_name="",
            jinja_env=None,
            settings=settings,
        )

    def render_certification(self, certification: Certification) -> None:
        """Render a single certification in the document.

        Args:
            certification: The Certification object containing the details of a single certification to render.

        Returns:
            None

        Notes:
            1. Extract references to the document and settings for convenience.
            2. Add a header for the certification section.
            3. If the settings require the issuer and the certification has an issuer, add the issuer to the document.
            4. If the settings require the name and the certification has a name, add the name to the document.
            5. If the settings require the issued date and the certification has an issued date, add the issued date to the document.
            6. If the settings require the expiration date and the certification has an expiration date, add the expiration date to the document.
            7. If the settings require the certification ID and the certification has a certification ID, add the certification ID to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("## Certification")

        if _settings.issuer and certification.issuer:
            _doc.add_text(f"Issuer: {certification.issuer}")
        if _settings.name and certification.name:
            _doc.add_text(f"Name: {certification.name}")
        if _settings.issued and certification.issued:
            _doc.add_text(f"Issued: {certification.issued}")
        if _settings.expires and certification.expires:
            _doc.add_text(f"Expires: {certification.expires}")
        if _settings.certification_id and certification.certification_id:
            _doc.add_text(f"Certification ID: {certification.certification_id}")

    def render(self) -> None:
        """Render the certifications section into the document.

        Args:
            None

        Returns:
            None

        Notes:
            1. Extract references to the document and certifications for convenience.
            2. If there are no certifications, log a debug message and return early.
            3. Log a debug message indicating that rendering has started.
            4. Add a top-level header for the certifications section.
            5. Iterate over each certification in the certifications list.
            6. For each certification, call the render_certification method to render its details.

        """
        # shortcuts
        _doc = self.document
        _certifications = self.certifications

        if not _certifications:
            log.debug("No certifications to render.")
            return

        log.debug("Rendering certifications.")

        _doc.add_header("# Certifications")

        for certification in _certifications.certifications:
            self.render_certification(certification)
