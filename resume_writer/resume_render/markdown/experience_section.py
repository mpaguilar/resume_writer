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

        _rendered = self.template.render(settings=self.settings, roles=self.roles)

        self.document.add_text(_rendered)


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

    def render(self) -> None:
        """Render projects section."""

        if len(self.projects) == 0:
            log.debug("No projects to render.")
            return

        log.debug("Rendering projects section.")
        _rendered = self.template.render(settings=self.settings, projects=self.projects)

        self.document.add_text(_rendered)


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

        self.document.add_text("# Experience")

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
