import logging
from pathlib import Path

from docx import Document
from docx_render.ats_certifications_section import ATSCertificationsSection
from docx_render.ats_education_section import ATSEducationSection
from docx_render.ats_personal_section import ATSPersonalSection
from docx_render.ats_roles_section import ATSRolesSection
from docx_render.resume_settings import (
    ResumeSettings,
)
from models.resume import Resume

log = logging.getLogger(__name__)


class ATSResume:
    """Represent and render an ATS-friendly Word resume."""

    def __init__(self, resume: Resume, settings: ResumeSettings | None):
        """Initialize a blank ATS-friendly Word document."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeSettings) or settings is None

        if settings is None:
            settings = ResumeSettings()

        ## end of settings

        self.settings = settings
        self.resume = resume
        self.document = Document()

    def render(self, path: Path) -> None:
        """Render an ATS-friendly Word document."""

        assert isinstance(path, Path)

        log.info(f"Rendering ATS friendly Word document to {path.as_posix()}")

        ATSPersonalSection(self.document, self.resume, self.settings.personal).render()

        if self.settings.render_education:
            ATSEducationSection(
                self.document,
                self.resume,
                self.settings.education,
            ).render()

        if self.settings.render_certifications:
            ATSCertificationsSection(
                self.document,
                self.resume,
                self.settings.certifications,
            ).render()

        if self.settings.render_roles:
            ATSRolesSection(self.document, self.resume, self.settings.roles).render()

        _path = Path(path)
        self.save(_path)

    def save(self, path: Path) -> None:
        """Save the document to a file."""
        self.document.save(path)
