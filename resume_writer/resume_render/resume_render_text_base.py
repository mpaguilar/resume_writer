import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jinja2 import Environment

from resume_writer.models.certifications import Certifications
from resume_writer.models.education import Education
from resume_writer.models.experience import (
    Experience,
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
from resume_writer.utils.text_doc import TextDoc

log = logging.getLogger(__name__)


class RenderBase:
    """Base class for rendering HTML files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    """

    def __init__(self, document: TextDoc, jinja_env: Environment | None):
        """Initialize superclass."""

        self.errors = []
        self.warnings = []

        assert isinstance(document, TextDoc)
        assert isinstance(jinja_env, (type(None), Environment))

        self.document = document
        self.jinja_env = jinja_env

    def save(self, path: Path) -> None:
        """Save the document to the given path."""
        with path.open("w") as f:
            f.write(self.document.text)

    def add_error(self, error: str) -> None:
        """Add an error to the list of errors."""
        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        """Add a warning to the list of warnings."""
        self.warnings.append(warning)


class ResumeRenderBase(RenderBase):
    """Base class for rendering resumes."""

    def __init__(
        self,
        document: TextDoc,
        jinja_env: Environment | None,
        resume: Resume,
        settings: ResumeRenderSettings | None,
    ):
        """Initialize superclass."""

        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings) or settings is None
        assert isinstance(document, TextDoc), f"document is {type(document)}"
        assert isinstance(jinja_env, (type(None),Environment))

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
        document: TextDoc,
        jinja_env: Environment,
        personal: Personal,
        template_name: str,
        settings: ResumePersonalSettings,
    ):
        """Initialize personal renderer."""

        assert isinstance(document, TextDoc), f"document is {type(document)}"
        assert isinstance(personal, Personal)
        assert isinstance(settings, ResumePersonalSettings)
        assert isinstance(template_name, str)

        super().__init__(document=document, jinja_env=jinja_env)

        self.settings = settings
        self.personal = personal
        if template_name:
            self.template = jinja_env.get_template(template_name)
        else:
            self.template = None


class ResumeRenderRolesBase(RenderBase):
    """Base class for rendering resume roles section."""

    def __init__(
        self,
        document: TextDoc,
        jinja_env: Environment | None,
        roles: Roles,
        template_name: str,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section."""

        super().__init__(document=document, jinja_env=jinja_env)
        assert isinstance(roles, Roles)
        assert isinstance(settings, ResumeRolesSettings)
        assert isinstance(template_name, str)
        assert isinstance(jinja_env, (type(None),Environment))

        self._roles = roles
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)
        else:
            self.template = None

    @property
    def roles(self) -> list[Role]:
        """Return roles which have not been filtered out."""
        _ret_roles = []
        for _role in self._roles:
            # Check if the role is older than the specified number of months
            if self.settings.months_ago and self.settings.months_ago > 0:
                _now = datetime.now(tz=timezone.utc)
                _end_date = _role.basics.end_date or _now
                _months_ago = _now - timedelta(days=self.settings.months_ago * 30)
                if _end_date < _months_ago:
                    continue
            _ret_roles.append(_role)
        return _ret_roles


class ResumeRenderProjectsBase(RenderBase):
    """Base class for rendering resume projects section."""

    def __init__(
        self,
        document: TextDoc,
        jinja_env: Environment,
        projects: Projects,
        template_name: str,
        settings: ResumeProjectsSettings,
    ):
        """Initialize the projects section."""
        super().__init__(document=document, jinja_env=jinja_env)
        assert isinstance(projects, Projects)
        assert isinstance(settings, ResumeProjectsSettings)
        assert isinstance(template_name, str)
        assert isinstance(jinja_env, (type(None),Environment))

        self.projects = projects
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)
        else:
            self.template = None


class ResumeRenderExperienceBase(RenderBase):
    """Base class for rendering resume experience section."""

    def __init__(
        self,
        document: TextDoc,
        jinja_env: Environment,
        experience: Experience,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section."""

        super().__init__(document=document, jinja_env=jinja_env)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeExperienceSettings)
        assert isinstance(jinja_env, (type(None),Environment))
        assert isinstance(document, TextDoc), f"document is {type(document)}"

        self.experience = experience
        self.document = document
        self.settings = settings
        self.jinja_env = jinja_env


class ResumeRenderEducationBase(RenderBase):
    """Base class for rendering resume education section."""

    def __init__(
        self,
        document: TextDoc,
        jinja_env: Environment,
        education: Education,
        template_name: str,
        settings: ResumeEducationSettings,
    ):
        """Initialize the education rendering section."""

        super().__init__(document=document, jinja_env=jinja_env)

        assert isinstance(education, Education)
        assert isinstance(settings, ResumeEducationSettings)
        assert isinstance(template_name, str)
        assert isinstance(jinja_env, (type(None),Environment))

        self.education = education
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)

    def degrees(self) -> None:
        """Render degrees section of education."""
        raise NotImplementedError

    def render(self) -> None:
        """Render education section."""
        raise NotImplementedError


class ResumeRenderCertificationsBase(RenderBase):
    """Base class for rendering resume certifications section."""

    def __init__(
        self,
        document: str,
        certifications: Certifications,
        jinja_env: Environment,
        template_name: str,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize certification renderer."""

        super().__init__(document=document, jinja_env=jinja_env)

        assert isinstance(certifications, Certifications)
        assert isinstance(settings, ResumeCertificationsSettings)
        assert isinstance(template_name, str)
        assert isinstance(jinja_env, (type(None),Environment))

        self.settings = settings
        self.certifications = certifications
        if template_name:
            self.template = jinja_env.get_template(template_name)


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
