import logging

from jinja2 import Environment

from resume_writer.models.experience import (
    Experience,
    Projects,
    Roles,
)
from resume_writer.resume_render.render_settings import (
    ResumeExperienceSettings,
    ResumeProjectsSettings,
    ResumeRolesSettings,
)
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderExperienceBase,
    ResumeRenderProjectsBase,
    ResumeRenderRolesBase,
)
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderRolesSection(ResumeRenderRolesBase):
    """Render experience roles section.

    This class is responsible for rendering a section of job roles within a resume
    using a Jinja2 template. It processes role data and outputs formatted HTML.

    Args:
        document (HtmlDoc): The HTML document object to which rendered content will be added.
        jinja_env (Environment): The Jinja2 environment used to render templates.
        roles (Roles): A collection of job roles to be rendered.
        settings (ResumeRolesSettings): Configuration settings for how roles should be rendered.

    Attributes:
        document (HtmlDoc): The HTML document where output will be added.
        jinja_env (Environment): Jinja2 environment for template rendering.
        roles (Roles): List of roles to render.
        template_name (str): Name of the Jinja2 template file for rendering roles.
        settings (ResumeRolesSettings): Rendering configuration for roles.

    Notes:
        1. Initializes the parent class with the provided document, Jinja2 environment,
           roles, template name, and settings.
        2. The `render` method checks if roles exist.
        3. If roles exist, it uses the Jinja2 template to render the roles with the given settings.
        4. The rendered content is added to the document using `add_text`.
        5. No disk, network, or database access is performed.

    Returns:
        None

    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        roles: Roles,
        settings: ResumeRolesSettings,
    ):
        """Initialize roles render object."""
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            roles=roles,
            template_name="roles.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render roles section.

        Renders the job roles section into the HTML document using a Jinja2 template.

        Args:
            None

        Returns:
            None: The method adds rendered HTML directly to the document.

        Notes:
            1. Checks if `self.roles` is empty; if so, logs a debug message and exits.
            2. Logs a debug message indicating rendering has started.
            3. Renders the Jinja2 template with `settings` and `roles` as context.
            4. Adds the rendered string to the document using `add_text`.
            5. No disk, network, or database access is used.

        """
        if not self.roles:
            log.debug("No roles to render.")

        log.debug("Rendering roles section.")

        _rendered = self.template.render(settings=self.settings, roles=self.roles)

        self.document.add_text(_rendered)


class RenderProjectsSection(ResumeRenderProjectsBase):
    """Render experience projects section.

    This class renders a section of projects associated with a resume using a Jinja2 template.

    Args:
        document (HtmlDoc): The HTML document object to which rendered content will be added.
        jinja_env (Environment): The Jinja2 environment used to render templates.
        projects (Projects): A collection of projects to be rendered.
        settings (ResumeProjectsSettings): Configuration settings for how projects should be rendered.

    Attributes:
        document (HtmlDoc): The HTML document where output will be added.
        jinja_env (Environment): Jinja2 environment for template rendering.
        projects (Projects): List of projects to render.
        template_name (str): Name of the Jinja2 template file for rendering projects.
        settings (ResumeProjectsSettings): Rendering configuration for projects.

    Notes:
        1. Initializes the parent class with the provided document, Jinja2 environment,
           projects, template name, and settings.
        2. The `render` method checks if projects exist.
        3. If projects exist, it uses the Jinja2 template to render the projects with the given settings.
        4. The rendered content is added to the document using `add_text`.
        5. No disk, network, or database access is performed.

    Returns:
        None

    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        projects: Projects,
        settings: ResumeProjectsSettings,
    ):
        """Initialize projects render object."""
        log.debug("Initializing projects render object.")

        super().__init__(
            document=document,
            jinja_env=jinja_env,
            projects=projects,
            template_name="projects.j2",
            settings=settings,
        )

    def render(self) -> None:
        """Render projects section.

        Renders the projects section into the HTML document using a Jinja2 template.

        Args:
            None

        Returns:
            None: The method adds rendered HTML directly to the document.

        Notes:
            1. Checks if `len(self.projects)` is zero; if so, logs a debug message and returns.
            2. Logs a debug message indicating rendering has started.
            3. Renders the Jinja2 template with `settings` and `projects` as context.
            4. Adds the rendered string to the document using `add_text`.
            5. No disk, network, or database access is used.

        """
        if len(self.projects) == 0:
            log.debug("No projects to render.")
            return

        log.debug("Rendering projects section.")
        _rendered = self.template.render(settings=self.settings, projects=self.projects)

        self.document.add_text(_rendered)


class RenderExperienceSection(ResumeRenderExperienceBase):
    """Render experience section.

    This class is responsible for rendering the entire experience section of a resume,
    including roles and projects, using a Jinja2 template. It aggregates data from
    `Experience`, and uses separate renderers for roles and projects.

    Args:
        document (HtmlDoc): The HTML document object to which rendered content will be added.
        jinja_env (Environment): The Jinja2 environment used to render templates.
        experience (Experience): The experience data (roles and projects) to be rendered.
        settings (ResumeExperienceSettings): Configuration settings for how experience should be rendered.

    Attributes:
        document (HtmlDoc): The HTML document where output will be added.
        jinja_env (Environment): Jinja2 environment for template rendering.
        experience (Experience): The experience data (roles and projects).
        settings (ResumeExperienceSettings): Rendering configuration for experience.

    Notes:
        1. Initializes the parent class with the provided document, Jinja2 environment,
           experience, and settings.
        2. Calculates the total number of items (roles + projects) to render.
        3. If no items are present, exits early.
        4. Adds an HTML heading "Experience" to the document.
        5. If roles are enabled in settings and `experience.roles` is not empty,
           creates and renders a `RenderRolesSection`.
        6. If projects are enabled in settings and `experience.projects` is not empty,
           creates and renders a `RenderProjectsSection`.
        7. No disk, network, or database access is performed.

    Returns:
        None

    """

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        experience: Experience,
        settings: ResumeExperienceSettings,
    ) -> None:
        """Initialize experience render object."""
        log.debug("Initializing experience render object.")
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            experience=experience,
            settings=settings,
        )

    def render(self) -> None:
        """Render experience section.

        Renders the experience section into the HTML document, including roles and projects.

        Args:
            None

        Returns:
            None: The method adds rendered HTML directly to the document.

        Notes:
            1. Calculates the total number of roles and projects that will be rendered.
            2. If no roles or projects exist, returns early.
            3. Adds an HTML heading "Experience" to the document.
            4. If roles are enabled and roles exist, creates and renders a `RenderRolesSection`.
            5. If projects are enabled and projects exist, creates and renders a `RenderProjectsSection`.
            6. No disk, network, or database access is used.

        """
        log.debug("Rendering experience section.")

        _experience_length = 0
        if self.settings.roles and self.experience.roles:
            _experience_length += len(self.experience.roles)

        if self.settings.projects and self.experience.projects:
            _experience_length += len(self.experience.projects)

        if _experience_length == 0:
            return

        self.document.add_text("<h1>Experience</h1>")

        if self.settings.roles and self.experience.roles:
            RenderRolesSection(
                document=self.document,
                jinja_env=self.jinja_env,
                roles=self.experience.roles,
                settings=self.settings.roles_settings,
            ).render()

        if self.settings.projects and self.experience.projects:
            RenderProjectsSection(
                document=self.document,
                jinja_env=self.jinja_env,
                projects=self.experience.projects,
                settings=self.settings.projects_settings,
            ).render()
