from pathlib import Path

import docx.document
from docx import Document
from docx_render.resume_settings import (
    ResumeCertificationsSettings,
    ResumeEducationSettings,
    ResumeExperienceSettings,
    ResumePersonalSettings,
    ResumeSettings,
)
from models.experience import RoleBasics, RoleSkills
from models.resume import Resume


class DocxRenderBase:
    """Base class for rendering docx files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    """

    def __init__(self):
        """Initialize superclass."""
        self.errors = []
        self.warnings = []


class DocxResumeBase(DocxRenderBase):
    """Base class for rendering resumes."""

    def __init__(self, resume: Resume, settings: ResumeSettings | None):
        """Initialize superclass."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeSettings) or settings is None
        if settings is None:
            settings = ResumeSettings()

        super().__init__()

        self.settings = settings
        self.resume = resume
        self.document = Document()

    def render(self) -> None:
        """Render Word document interface."""
        return NotImplemented

    def save(self, path: Path) -> None:
        """Save the document to a file."""
        self.document.save(path)


class DocxPersonalBase(DocxRenderBase):
    """Base class for rendering resume personal section."""

    def __init__(
        self,
        document: Document,
        resume: Resume,
        settings: ResumePersonalSettings,
    ):
        """Initialize personal renderer."""

        assert isinstance(document, docx.document.Document)
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumePersonalSettings)

        super().__init__()

        self.settings = settings
        self.document = document
        self.resume = resume

    def contact_info(self) -> None:
        """Render contact information."""
        return NotImplemented

    def website_info(self) -> None:
        """Render website information."""
        return NotImplemented

    def visa_status(self) -> None:
        """Render visa status."""
        return NotImplemented

    def banner(self) -> None:
        """Render banner."""
        return NotImplemented

    def note(self) -> None:
        """Render note."""
        return NotImplemented

    def render(self) -> None:
        """Render personal section."""
        return NotImplemented


class DocxExperienceBase(DocxRenderBase):
    """Base class for rendering resume experience section."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeExperienceSettings,
    ):
        """Initialize the roles section."""

        super().__init__()
        assert isinstance(resume, Resume)
        assert isinstance(document, docx.document.Document)
        assert isinstance(settings, ResumeExperienceSettings)

        self.resume = resume
        self.document = document
        self.settings = settings

    # TODO: is there a better way to do this so the noqa isn't necessary?
    def basics(self, basics: RoleBasics) -> None:  # noqa: ARG002
        """Render basic section of experience."""
        return NotImplemented

    def skills(self, skills: RoleSkills) -> None:  # noqa: ARG002
        """Render skills section of experience."""
        return NotImplemented

    def roles(self) -> None:
        """Render roles section of experience."""
        return NotImplemented

    def render(self) -> None:
        """Render experience section."""
        return NotImplemented


class DocxEducationBase(DocxRenderBase):
    """Base class for rendering resume education section."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeEducationSettings,
    ):
        """Initialize the education rendering section."""
        assert isinstance(document, docx.document.Document)
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeEducationSettings)

        self.document = document
        self.resume = resume
        self.settings = settings

    def degrees(self) -> None:
        """Render degrees section of education."""
        return NotImplemented

    def render(self) -> None:
        """Render education section."""
        return NotImplemented


class DocxCertificationsBase(DocxRenderBase):
    """Base class for rendering resume certifications section."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize certification renderer."""

        assert isinstance(document, docx.document.Document)
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.document = document
        self.settings = settings
        self.resume = resume

    def certifications(self) -> None:
        """Render certifications section of resume."""
        return NotImplemented

    def render(self) -> None:
        """Render certifications section."""
        return NotImplemented
