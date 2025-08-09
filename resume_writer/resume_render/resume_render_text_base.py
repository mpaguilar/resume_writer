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

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.

    Attributes:
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.

    Notes:
        1. Initializes the errors and warnings lists as empty.
        2. Validates that the document is an instance of TextDoc.
        3. Validates that jinja_env is either None or an instance of Environment.
        4. Assigns the provided document and jinja_env to instance attributes.

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
        """Save the document to the given path.

        Args:
            path (Path): The file system path to save the document.

        Returns:
            None

        Notes:
            1. Opens the file at the given path in write mode.
            2. Writes the document's text content to the file.
            3. Closes the file.

        """
        with path.open("w") as f:
            f.write(self.document.text)

    def add_error(self, error: str) -> None:
        """Add an error to the list of errors.

        Args:
            error (str): The error message to add.

        Returns:
            None

        Notes:
            1. Appends the error message to the errors list.

        """
        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        """Add a warning to the list of warnings.

        Args:
            warning (str): The warning message to add.

        Returns:
            None

        Notes:
            1. Appends the warning message to the warnings list.

        """
        self.warnings.append(warning)


class ResumeRenderBase(RenderBase):
    """Base class for rendering resumes.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.
        resume (Resume): The resume data to be rendered.
        settings (ResumeRenderSettings | None): The rendering settings for the resume.

    Attributes:
        settings (ResumeRenderSettings): The rendering settings for the resume.
        resume (Resume): The resume data to be rendered.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.

    Notes:
        1. Validates that resume is an instance of Resume.
        2. Validates that settings is either None or an instance of ResumeRenderSettings.
        3. Validates that document is an instance of TextDoc.
        4. Validates that jinja_env is either None or an instance of Environment.
        5. If settings is None, initializes settings with a new ResumeRenderSettings instance.
        6. Calls the superclass constructor to initialize common attributes.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))

        if settings is None:
            settings = ResumeRenderSettings()

        super().__init__(document=document, jinja_env=jinja_env)

        self.settings = settings
        self.resume = resume


class ResumeRenderPersonalBase(RenderBase):
    """Base class for rendering resume personal section.

    This class handles rendering of personal information such as name, contact details, and profile summary.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        personal (Personal): The personal data to be rendered.
        template_name (str): The name of the Jinja2 template to use for rendering.
        settings (ResumePersonalSettings): The rendering settings for the personal section.

    Attributes:
        settings (ResumePersonalSettings): The rendering settings for the personal section.
        personal (Personal): The personal data to be rendered.
        template (Template | None): The Jinja2 template for rendering, if template_name is provided.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.

    Notes:
        1. Validates that document is an instance of TextDoc.
        2. Validates that personal is an instance of Personal.
        3. Validates that settings is an instance of ResumePersonalSettings.
        4. Validates that template_name is a string.
        5. Calls the superclass constructor to initialize common attributes.
        6. Assigns the provided settings and personal data to instance attributes.
        7. If template_name is provided, loads the corresponding Jinja2 template.

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
    """Base class for rendering resume roles section.

    This class handles filtering and rendering of job roles based on time constraints.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.
        roles (Roles): The list of job roles to be rendered.
        template_name (str): The name of the Jinja2 template to use for rendering.
        settings (ResumeRolesSettings): The rendering settings for the roles section.

    Attributes:
        _roles (Roles): The list of job roles to be rendered.
        settings (ResumeRolesSettings): The rendering settings for the roles section.
        template (Template | None): The Jinja2 template for rendering, if template_name is provided.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment | None): The Jinja2 environment for template rendering.

    Notes:
        1. Validates that document is an instance of TextDoc.
        2. Validates that roles is an instance of Roles.
        3. Validates that settings is an instance of ResumeRolesSettings.
        4. Validates that template_name is a string.
        5. Validates that jinja_env is either None or an instance of Environment.
        6. Calls the superclass constructor to initialize common attributes.
        7. Assigns the provided roles and settings to instance attributes.
        8. If template_name is provided, loads the corresponding Jinja2 template.

    Returns:
        list[Role]: A list of roles that have not been filtered out based on the time constraint.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))

        self._roles = roles
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)
        else:
            self.template = None

    @property
    def roles(self) -> list[Role]:
        """Return roles which have not been filtered out.

        Returns:
            list[Role]: A list of roles that are not older than the specified number of months.

        Notes:
            1. Initializes an empty list to store filtered roles.
            2. Iterates over each role in the _roles list.
            3. If the settings specify a number of months ago, checks if the role's end date is older than that time.
            4. If the role is older than the specified time, skips it.
            5. Otherwise, adds the role to the filtered list.
            6. Returns the filtered list of roles.

        """
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


class ResumeRenderProjectsBase(RenderBase):
    """Base class for rendering resume projects section.

    This class handles rendering of projects based on provided settings.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        projects (Projects): The list of projects to be rendered.
        template_name (str): The name of the Jinja2 template to use for rendering.
        settings (ResumeProjectsSettings): The rendering settings for the projects section.

    Attributes:
        projects (Projects): The list of projects to be rendered.
        settings (ResumeProjectsSettings): The rendering settings for the projects section.
        template (Template | None): The Jinja2 template for rendering, if template_name is provided.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.

    Notes:
        1. Validates that document is an instance of TextDoc.
        2. Validates that projects is an instance of Projects.
        3. Validates that settings is an instance of ResumeProjectsSettings.
        4. Validates that template_name is a string.
        5. Validates that jinja_env is either None or an instance of Environment.
        6. Calls the superclass constructor to initialize common attributes.
        7. Assigns the provided projects and settings to instance attributes.
        8. If template_name is provided, loads the corresponding Jinja2 template.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))

        self.projects = projects
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)
        else:
            self.template = None


class ResumeRenderExperienceBase(RenderBase):
    """Base class for rendering resume experience section.

    This class handles rendering of experience sections, including roles.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        experience (Experience): The experience data to be rendered.
        settings (ResumeRolesSettings): The rendering settings for the roles section.

    Attributes:
        experience (Experience): The experience data to be rendered.
        settings (ResumeRolesSettings): The rendering settings for the roles section.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.

    Notes:
        1. Validates that experience is an instance of Experience.
        2. Validates that settings is an instance of ResumeExperienceSettings.
        3. Validates that jinja_env is either None or an instance of Environment.
        4. Validates that document is an instance of TextDoc.
        5. Calls the superclass constructor to initialize common attributes.
        6. Assigns the provided experience and settings to instance attributes.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))
        assert isinstance(document, TextDoc), f"document is {type(document)}"

        self.experience = experience
        self.document = document
        self.settings = settings
        self.jinja_env = jinja_env


class ResumeRenderEducationBase(RenderBase):
    """Base class for rendering resume education section.

    This class handles rendering of educational qualifications.

    Args:
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        education (Education): The education data to be rendered.
        template_name (str): The name of the Jinja2 template to use for rendering.
        settings (ResumeEducationSettings): The rendering settings for the education section.

    Attributes:
        education (Education): The education data to be rendered.
        settings (ResumeEducationSettings): The rendering settings for the education section.
        template (Template | None): The Jinja2 template for rendering, if template_name is provided.
        document (TextDoc): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.

    Notes:
        1. Validates that education is an instance of Education.
        2. Validates that settings is an instance of ResumeEducationSettings.
        3. Validates that template_name is a string.
        4. Validates that jinja_env is either None or an instance of Environment.
        5. Calls the superclass constructor to initialize common attributes.
        6. Assigns the provided education and settings to instance attributes.
        7. If template_name is provided, loads the corresponding Jinja2 template.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))

        self.education = education
        self.settings = settings
        if template_name:
            self.template = jinja_env.get_template(template_name)

    def degrees(self) -> None:
        """Render degrees section of education.

        Returns:
            None

        Notes:
            1. This method is currently a placeholder and not implemented.

        """
        raise NotImplementedError

    def render(self) -> None:
        """Render education section.

        Returns:
            None

        Notes:
            1. This method is currently a placeholder and not implemented.

        """
        raise NotImplementedError


class ResumeRenderCertificationsBase(RenderBase):
    """Base class for rendering resume certifications section.

    This class handles rendering of certifications based on provided settings.

    Args:
        document (str): The text document to be rendered.
        certifications (Certifications): The certifications data to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        template_name (str): The name of the Jinja2 template to use for rendering.
        settings (ResumeCertificationsSettings): The rendering settings for the certifications section.

    Attributes:
        settings (ResumeCertificationsSettings): The rendering settings for the certifications section.
        certifications (Certifications): The certifications data to be rendered.
        template (Template | None): The Jinja2 template for rendering, if template_name is provided.
        document (str): The text document to be rendered.
        jinja_env (Environment): The Jinja2 environment for template rendering.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.

    Notes:
        1. Validates that certifications is an instance of Certifications.
        2. Validates that settings is an instance of ResumeCertificationsSettings.
        3. Validates that template_name is a string.
        4. Validates that jinja_env is either None or an instance of Environment.
        5. Calls the superclass constructor to initialize common attributes.
        6. Assigns the provided settings and certifications to instance attributes.
        7. If template_name is provided, loads the corresponding Jinja2 template.

    """

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
        assert isinstance(jinja_env, (type(None), Environment))

        self.settings = settings
        self.certifications = certifications
        if template_name:
            self.template = jinja_env.get_template(template_name)


class ResumeRenderExecutiveSummaryBase(RenderBase):
    """Base class for rendering resume executive summary section.

    This class handles rendering of executive summary based on experience data.

    Args:
        document (str): The text document to be rendered.
        experience (Experience): The experience data to be used for generating the summary.
        settings (ResumeExecutiveSummarySettings): The rendering settings for the executive summary.

    Attributes:
        experience (Experience): The experience data to be used for generating the summary.
        document (str): The text document to be rendered.
        settings (ResumeExecutiveSummarySettings): The rendering settings for the executive summary.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.

    Notes:
        1. Validates that experience is an instance of Experience.
        2. Validates that settings is an instance of ResumeExecutiveSummarySettings.
        3. Calls the superclass constructor to initialize common attributes.
        4. Assigns the provided experience and settings to instance attributes.

    """

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
    """Base class for rendering resume skills matrix section.

    This class handles rendering of skills matrix based on experience data.

    Args:
        document (str): The text document to be rendered.
        experience (Experience): The experience data to be used for generating the skills matrix.
        settings (ResumeSkillsMatrixSettings): The rendering settings for the skills matrix.

    Attributes:
        experience (Experience): The experience data to be used for generating the skills matrix.
        document (str): The text document to be rendered.
        settings (ResumeSkillsMatrixSettings): The rendering settings for the skills matrix.
        errors (list[str]): List of errors encountered during rendering.
        warnings (list[str]): List of warnings encountered during rendering.

    Notes:
        1. Validates that experience is an instance of Experience.
        2. Validates that settings is an instance of ResumeSkillsMatrixSettings.
        3. Calls the superclass constructor to initialize common attributes.
        4. Assigns the provided experience and settings to instance attributes.

    """

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
