from pathlib import Path

import docx.document

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.models.education import Degree, Education
from resume_writer.models.experience import (
    Experience,
    Project,
    Projects,
    Role,
    Roles,
)
from resume_writer.models.personal import Personal
from resume_writer.models.resume import Resume
from resume_writer.resume_render.render_settings import (
    ResumeCertificationsSettings,
    ResumeEducationSettings,
    ResumeExperienceSettings,
    ResumePersonalSettings,
    ResumeProjectsSettings,
    ResumeRolesSettings,
    ResumeSettings,
)


class RenderBase:
    """Base class for rendering docx files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    """

    def __init__(self):
        """Initialize superclass."""
        self.errors = []
        self.warnings = []


class ResumeRenderBase(RenderBase):
    """Base class for rendering resumes."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeSettings | None,
    ):
        """Initialize superclass."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeSettings) or settings is None
        if settings is None:
            settings = ResumeSettings()

        super().__init__()

        self.settings = settings
        self.resume = resume
        self.document = document

    def render(self) -> None:
        """Render Word document interface."""
        raise NotImplementedError

    def save(self, path: Path) -> None:
        """Save the document to a file."""
        self.document.save(path)


class ResumeRenderPersonalBase(RenderBase):
    """Base class for rendering resume personal section.

    Document : a python-docx Document object or a list of strings
    """

    def __init__(
        self,
        document: docx.document.Document | list[str],
        personal: Personal,
        settings: ResumePersonalSettings,
    ):
        """Initialize personal renderer."""

        assert isinstance(document, (docx.document.Document, list))
        if isinstance(document, list):
            assert all(isinstance(item, str) for item in document)
        assert isinstance(personal, Personal)
        assert isinstance(settings, ResumePersonalSettings)

        super().__init__()

        self.settings = settings
        self.document = document
        self.personal = personal


class ResumeRenderRolesBase(RenderBase):
    """Base class for rendering resume roles section."""

    def __init__(
        self,
        document: docx.document.Document,
        roles: Roles,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section."""

        super().__init__()

        assert isinstance(document, docx.document.Document)
        assert isinstance(roles, Roles)
        assert isinstance(settings, ResumeRolesSettings)

        self.document = document
        self.roles = roles
        self.settings = settings


class ResumeRenderRoleBase(RenderBase):
    """Base class for rendering resume role section."""

    def __init__(
        self,
        document: docx.document.Document,
        role: Role,
        settings: ResumeRolesSettings,
    ):
        """Initialize the role section."""
        super().__init__()
        assert isinstance(document, docx.document.Document)
        assert isinstance(role, Role)
        assert isinstance(settings, ResumeRolesSettings)

        self.document = document
        self.role = role
        self.settings = settings


class ResumeRenderProjectsBase(RenderBase):
    """Base class for rendering resume projects section."""

    def __init__(
        self,
        document: docx.document.Document,
        projects: Projects,
        settings: ResumeProjectsSettings,
    ):
        """Initialize the projects section."""
        super().__init__()
        assert isinstance(document, docx.document.Document)
        assert isinstance(projects, Projects)
        assert isinstance(settings, ResumeProjectsSettings)

        self.document = document
        self.projects = projects
        self.settings = settings


class ResumeRenderProjectBase(RenderBase):
    """Base class for rendering resume project section."""

    def __init__(
        self,
        document: docx.document.Document,
        project: Project,
        settings: ResumeProjectsSettings,
    ):
        """Initialize the project section."""
        super().__init__()
        assert isinstance(document, docx.document.Document)
        assert isinstance(project, Project)
        assert isinstance(settings, ResumeProjectsSettings)

        self.document = document
        self.project = project
        self.settings = settings


class ResumeRenderExperienceBase(RenderBase):
    """Base class for rendering resume experience section."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section."""

        super().__init__()
        assert isinstance(experience, Experience)
        assert isinstance(document, docx.document.Document)
        assert isinstance(settings, ResumeExperienceSettings)

        self.experience = experience
        self.document = document
        self.settings = settings


class ResumeRenderDegreeBase(RenderBase):
    """Base class for rendering a single degree."""

    def __init__(
        self,
        document: docx.document.Document,
        degree: Degree,
        settings: ResumeEducationSettings,
    ):
        """Initialize the degree section."""
        assert isinstance(document, docx.document.Document)
        assert isinstance(degree, Degree)
        assert isinstance(settings, ResumeEducationSettings)

        self.degree = degree
        self.document = document
        self.settings = settings


class ResumeRenderEducationBase(RenderBase):
    """Base class for rendering resume education section."""

    def __init__(
        self,
        document: docx.document.Document,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the education rendering section."""
        assert isinstance(document, docx.document.Document)
        assert isinstance(education, Education)
        assert isinstance(settings, ResumeEducationSettings)

        self.document = document
        self.education = education
        self.settings = settings

    def degrees(self) -> None:
        """Render degrees section of education."""
        raise NotImplementedError

    def render(self) -> None:
        """Render education section."""
        raise NotImplementedError

class ResumeRenderCertificationBase(RenderBase):
    """Base class for rendering a single certification."""

    def __init__(
        self,
        document: docx.document.Document,
        certification: Certification,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the certification section."""
        assert isinstance(document, docx.document.Document)
        assert isinstance(certification, Certification)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.document = document
        self.certification = certification
        self.settings = settings

class ResumeRenderCertificationsBase(RenderBase):
    """Base class for rendering resume certifications section."""

    def __init__(
        self,
        document: docx.document.Document,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize certification renderer."""

        assert isinstance(document, docx.document.Document)
        assert isinstance(certifications, Certifications)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.document = document
        self.settings = settings
        self.certifications = certifications
