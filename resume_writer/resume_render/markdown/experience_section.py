import logging

from jinja2 import Environment

from resume_writer.models.experience import (
    Experience,
    Project,
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
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderRolesSection(ResumeRenderRolesBase):
    """Render experience roles section."""

    def __init__(
        self,
        document: MarkdownDoc,
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
        """Render roles section."""

        if not self.roles:
            log.debug("No roles to render.")

        log.debug("Rendering roles section.")


class RenderProjectsSection(ResumeRenderProjectsBase):
    """Render experience projects section."""

    def __init__(
        self,
        document: MarkdownDoc,
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

    def render_project(self, project: Project) -> None:
        """Render a single project."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("### Project")

        _doc.add_header("#### Overview")

        if _settings.title and project.overview.title:
            _doc.add_text(f"Title: {project.overview.title}")
        if _settings.url and project.overview.url:
            _doc.add_text(f"URL: {project.overview.url}")
        if _settings.url_description and project.overview.url_description:
            _doc.add_text(f"URL Description: {project.overview.url_description}")
        if _settings.start_date and project.overview.start_date:
            _doc.add_text(f"Start Date: {project.overview.start_date}")
        if _settings.end_date and project.overview.end_date:
            _doc.add_text(f"End Date: {project.overview.end_date}")

        if _settings.description and project.description.text:
            _doc.add_header("#### Description")
            _doc.add_text(f"{project.description.text}")

        if _settings.skills and project.skills:
            _doc.add_header("#### Skills")
            for skill in project.skills:
                _doc.add_text(f"* {skill}")

    def render(self) -> None:
        """Render projects section."""
        # shortcuts
        _doc = self.document
        _settings = self.settings
        _projects = self.projects

        if len(_projects) == 0:
            log.debug("No projects to render.")
            return

        log.debug("Rendering projects section.")

        _doc.add_header("## Projects")

        for project in _projects:
            self.render_project(project)


class RenderExperienceSection(ResumeRenderExperienceBase):
    """Render experience section."""

    def __init__(
        self,
        document: MarkdownDoc,
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
        """Render experience section."""

        log.debug("Rendering experience section.")

        self.document.add_header("# Experience")

        if self.settings.projects and self.experience.projects:
            RenderProjectsSection(
                document=self.document,
                jinja_env=self.jinja_env,
                projects=self.experience.projects,
                settings=self.settings.projects_settings,
            ).render()

        if self.settings.roles and self.experience.roles:
            RenderRolesSection(
                document=self.document,
                jinja_env=self.jinja_env,
                roles=self.experience.roles,
                settings=self.settings.roles_settings,
            ).render()
