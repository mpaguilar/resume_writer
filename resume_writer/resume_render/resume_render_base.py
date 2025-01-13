from datetime import datetime, timedelta, timezone
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
    ResumeExecutiveSummarySettings,
    ResumeExperienceSettings,
    ResumePersonalSettings,
    ResumeProjectsSettings,
    ResumeRenderSettings,
    ResumeRolesSettings,
    ResumeSkillsMatrixSettings,
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

        # font size should always be set. Other classes use it for scaling.
        # If it isn't set, the other classes will fail.
        if not _font.size:
            _font.size = Pt(12)

        # put the font-size into the class, so subclasses easily use it
        if _normal.font.size:
            self.font_size = _normal.font.size.pt
        else:
            raise ValueError("Normal style font size not set.")

    def add_horizontal_line(self, paragraph: Paragraph, offset: int = 0) -> None:
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
        settings: ResumeRenderSettings | None,
    ):
        """Initialize superclass."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings) or settings is None

        if settings is None:
            settings = ResumeRenderSettings()

        super().__init__(document=document)

        self.settings = settings
        self.resume = resume

        _normal = self.document.styles["Normal"]

        _normal.paragraph_format.space_before = Pt(0)
        _normal.paragraph_format.space_after = Pt(0)

        _font = _normal.font

        if self.settings.font_size:
            _font.size = Pt(int(self.settings.font_size))

        # margins are set per-section
        _section = self.document.sections[0]

        if self.settings.margin_width:
            _section.left_margin = Inches(float(self.settings.margin_width))
            _section.right_margin = Inches(float(self.settings.margin_width))

        if self.settings.bottom_margin:
            _section.bottom_margin = Inches(float(self.settings.bottom_margin))

        if self.settings.top_margin:
            _section.top_margin = Inches(float(self.settings.top_margin))

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

        self._roles = roles
        self.settings = settings

    @property
    def roles(self) -> list[Role]:
        """Return roles which have not been filtered out."""
        _ret_roles = []
        for _role in self._roles:
            # Check if the role is older than the specified number of months
            if self.settings.months_ago and int(self.settings.months_ago) > 0:
                _now = datetime.now(tz=timezone.utc)
                _end_date = _role.basics.end_date or _now
                _months_ago = _now - timedelta(days=int(self.settings.months_ago) * 30)
                if _end_date < _months_ago:
                    continue
            _ret_roles.append(_role)
        return _ret_roles


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


class ResumeRenderExecutiveSummaryBase(RenderBase):
    """Base class for rendering resume executive summary section."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeExecutiveSummarySettings,
    ) -> None:
        """Initialize the executive summary section."""

        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeExecutiveSummarySettings)
        self.experience = experience
        self.document = document
        self.settings = settings


class ResumeRenderSkillsMatrixBase(RenderBase):
    """Base class for rendering resume skills matrix section."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeSkillsMatrixSettings,
    ) -> None:
        """Initialize the skills matrix section."""

        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeSkillsMatrixSettings)
        self.experience = experience
        self.document = document
        self.settings = settings
