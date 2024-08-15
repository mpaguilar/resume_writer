from pathlib import Path

import docx.document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

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

    def __init__(self, document: docx.document.Document):
        """Initialize superclass."""

        self.errors = []
        self.warnings = []

        self.document = document

        _normal = self.document.styles["Normal"]
        _font = _normal.font
        _font.size = Pt(10)

        _section = self.document.sections[0]
        _section.left_margin = Inches(0.5)
        _section.right_margin = Inches(0.5)

        _normal.paragraph_format.space_before = Pt(0)
        _normal.paragraph_format.space_after = Pt(0)

        if _normal.font.size:
            self.font_size = _normal.font.size.pt
        else:
            raise ValueError("Normal style font size not set.")

    def add_horizontal_line(self, paragraph : Paragraph, offset : int = 0) -> None:
        """Add a horizontal line to a document."""

        p = paragraph._element  # noqa: SLF001
        p_pr = p.get_or_add_pPr()
        p_borders = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "auto")
        p_borders.append(bottom)
        p_pr.append(p_borders)
        paragraph.paragraph_format.left_indent = Inches(offset)
        paragraph.paragraph_format.right_indent = Inches(offset)


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

        super().__init__(document=document)

        self.settings = settings
        self.resume = resume

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

        super().__init__(document=document)

        self.settings = settings
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

        super().__init__(document=document)

        assert isinstance(roles, Roles)
        assert isinstance(settings, ResumeRolesSettings)

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
        super().__init__(document=document)
        assert isinstance(role, Role)
        assert isinstance(settings, ResumeRolesSettings)

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
        super().__init__(document=document)
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
        super().__init__(document=document)
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

        super().__init__(document=document)
        assert isinstance(experience, Experience)
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
        assert isinstance(degree, Degree)
        assert isinstance(settings, ResumeEducationSettings)

        super().__init__(document=document)

        self.degree = degree
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

        super().__init__(document=document)

        assert isinstance(education, Education)
        assert isinstance(settings, ResumeEducationSettings)

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

        super().__init__(document=document)

        assert isinstance(certification, Certification)
        assert isinstance(settings, ResumeCertificationsSettings)

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

        super().__init__(document=document)

        assert isinstance(certifications, Certifications)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.settings = settings
        self.certifications = certifications
