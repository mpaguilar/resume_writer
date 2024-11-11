import logging

from jinja2 import Environment

from resume_writer.models.certifications import Certifications
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
        jinja_env: Environment,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the basic certifications renderer."""
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            certifications=certifications,
            template_name="certifications.j2",
            settings=settings,
        )

    def render_certification(self, certification) -> None:
        """Render a single certification."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("## Certification")
        
        if _settings.name and certification.name:
            _doc.add_text(f"Name: {certification.name}")
        if _settings.issuer and certification.issuer:
            _doc.add_text(f"Issuer: {certification.issuer}")
        if _settings.issued and certification.issued:
            _doc.add_text(f"Issued: {certification.issued}")
        if _settings.expires and certification.expires:
            _doc.add_text(f"Expires: {certification.expires}")
        if _settings.certification_id and certification.certification_id:
            _doc.add_text(f"Certification ID: {certification.certification_id}")

    def render(self) -> None:
        """Render the certifications section."""
        # shortcuts
        _doc = self.document
        _settings = self.settings
        _certifications = self.certifications

        if not _certifications:
            log.debug("No certifications to render.")
            return

        log.debug("Rendering certifications.")

        _doc.add_header("# Certifications")

        for certification in _certifications.certifications:
            self.render_certification(certification)
