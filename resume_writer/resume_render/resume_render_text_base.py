import logging
from pathlib import Path

from jinja2 import Environment
from utils.html_doc import HtmlDoc

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.models.education import Education
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

log = logging.getLogger(__name__)


class RenderBase:
    """Base class for rendering HTML files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    """

    def __init__(self, document: HtmlDoc, jinja_env : Environment):
        """Initialize superclass."""

        self.errors = []
        self.warnings = []

        assert isinstance(document, HtmlDoc)
        assert isinstance(jinja_env, Environment)

        self.document = document
        self.jinja_env = jinja_env

    def save(self, path: Path) -> None:
        """Save the document to the given path."""
        with path.open("w") as f:
            f.write(self.document.text)

class ResumeRenderBase(RenderBase):
    """Base class for rendering resumes."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env : Environment,
        resume: Resume,
        settings: ResumeRenderSettings | None,
    ):
        """Initialize superclass."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings) or settings is None
        assert isinstance(document, HtmlDoc), f"document is {type(document)}"
        assert isinstance(jinja_env, Environment)

        if settings is None:
            settings = ResumeRenderSettings()

        super().__init__(document=document, jinja_env=jinja_env)

        self.settings = settings
        self.resume = resume




class ResumeRenderPersonalBase(RenderBase):
    """Base class for rendering resume personal section.

    Document : a python-docx Document object or a list of strings
    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env : Environment,
        personal: Personal,
        template_name: str,
        settings: ResumePersonalSettings,
    ):
        """Initialize personal renderer."""

        assert isinstance(document, HtmlDoc), f"document is {type(document)}"
        assert isinstance(personal, Personal)
        assert isinstance(settings, ResumePersonalSettings)
        assert isinstance(template_name, str)

        super().__init__(document=document, jinja_env=jinja_env)

        self.settings = settings
        self.personal = personal
        self.template = jinja_env.get_template(template_name)


class ResumeRenderRolesBase(RenderBase):
    """Base class for rendering resume roles section."""

    def __init__(
        self,
        document: str,
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
        document: str,
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
        document: str,
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
        document: str,
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
        document: str,
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


class ResumeRenderEducationBase(RenderBase):
    """Base class for rendering resume education section."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env : Environment,
        education: Education,
        template_name: str,
        settings: ResumeEducationSettings,
    ):
        """Initialize the education rendering section."""

        super().__init__(document=document, jinja_env=jinja_env)

        assert isinstance(education, Education)
        assert isinstance(settings, ResumeEducationSettings)
        assert isinstance(template_name, str)
        assert isinstance(jinja_env, Environment)

        self.education = education
        self.settings = settings
        self.template = jinja_env.get_template(template_name)

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
        document: str,
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
        document: str,
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
        document: str,
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
        document: str,
        experience : Experience,
        settings: ResumeSkillsMatrixSettings,
    ) -> None:
        """Initialize the skills matrix section."""

        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeSkillsMatrixSettings)
        self.experience = experience
        self.document = document
        self.settings = settings
