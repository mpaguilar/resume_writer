import logging
from datetime import datetime

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches, Pt

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

    def render(self) -> None:
        """Render the certification section."""

        _certification = self.certification

        _paragraph = self.document.add_paragraph()
        _paragraph.paragraph_format.space_after = Pt(1)

        _tab_stop_right = Inches(7.4)
        _tab_stops = _paragraph.paragraph_format.tab_stops

        _tab_stops.add_tab_stop(
            _tab_stop_right,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.SPACES,
        )

        if _certification.name and self.settings.name:
            _run = _paragraph.add_run(f"{_certification.name}")
            _run.bold = True

        if _certification.issuer and self.settings.issuer:
            if _certification.name and self.settings.name:
                _paragraph.add_run("\t")
            _paragraph.add_run(f"{_certification.issuer}")

        if _certification.issued and self.settings.issued:
            if (_certification.name and self.settings.name) or (
                _certification.issuer and self.settings.issuer
            ):
                _paragraph.add_run("\n")
            _value = datetime.strftime(_certification.issued, "%B %Y")
            _paragraph.add_run(f"Issued: {_value}")

        if _certification.expires and self.settings.expires:
            if _certification.issued and self.settings.issued:
                _paragraph.add_run(" - ")
            _value = datetime.strftime(_certification.expires, "%B %Y")
            _paragraph.add_run(f"Expires: {_value}")


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

        """

        log.info("Rendering Certifications section.")

        if len(self.certifications) > 0:
            self.document.add_heading("Certifications", level=2)
        else:
            return

        for _certification in self.certifications:
            RenderCertificationSection(
                self.document,
                _certification,
                self.settings,
            ).render()
