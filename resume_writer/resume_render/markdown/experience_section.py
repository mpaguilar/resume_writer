import logging

from jinja2 import Environment

from resume_writer.models.experience import (
    Experience,
    Project,
    Projects,
    Role,
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
from resume_writer.utils.date_format import format_date
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

    def render_basics(self, role: Role) -> None:
        """Render role basics."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("#### Basics")
        if role.basics.company:  # company is required
            _doc.add_text(f"Company: {role.basics.company}")
        if _settings.agency_name and role.basics.agency_name:
            _doc.add_text(f"Agency: {role.basics.agency_name}")
        if _settings.job_category and role.basics.job_category:
            _doc.add_text(f"Job category: {role.basics.job_category}")
        if _settings.employment_type and role.basics.employment_type:
            _doc.add_text(f"Employment type: {role.basics.employment_type}")
        if _settings.start_date and role.basics.start_date:
            _doc.add_text(f"Start date: {format_date(role.basics.start_date)}")
        if _settings.end_date and role.basics.end_date:
            _doc.add_text(f"End date: {format_date(role.basics.end_date)}")
        if role.basics.title:  # title is required
            _doc.add_text(f"Title: {role.basics.title}")
        if _settings.reason_for_change and role.basics.reason_for_change:
            _doc.add_text(f"Reason for change: {role.basics.reason_for_change}")
        if _settings.location and role.basics.location:
            _doc.add_text(f"Location: {role.basics.location}")

    def render_highlights(self, role: Role) -> None:
        """Render role highlights."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.highlights and role.highlights:
            _doc.add_header("#### Highlights")
            for highlight in role.highlights:
                _doc.add_text(f"- {highlight}")

    def render_responsibilities(self, role: Role) -> None:
        """Render role responsibilities."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.responsibilities and role.responsibilities:
            _doc.add_header("#### Responsibilities")
            for responsibility in role.responsibilities:
                _doc.add_text(f"- {responsibility}")

    def render_skills(self, role: Role) -> None:
        """Render role skills."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.skills and role.skills:
            _doc.add_header("#### Skills")
            for skill in role.skills:
                _doc.add_text(f"- {skill}")

    def render_projects(self, role: Role) -> None:
        """Render role projects."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.projects and role.projects:
            _doc.add_header("#### Projects")
            for project in role.projects:
                _doc.add_text(f"- {project}")

    def render_role(self, role: Role) -> None:
        """Render a single role."""
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("### Role")

        self.render_basics(role)

        if _settings.summary and role.summary and role.summary.summary:
            _doc.add_header("#### Summary")
            _doc.add_text(role.summary.summary)

        if (
            _settings.responsibilities
            and role.responsibilities
            and role.responsibilities.text
        ):
            _doc.add_header("#### Responsibilities")
            _doc.add_text(role.responsibilities.text)

        if _settings.skills and role.skills:
            _doc.add_header("#### Skills")
            for skill in role.skills:
                _doc.add_text(f"* {skill}")

    def render(self) -> None:
        """Render roles section."""
        # shortcuts
        _doc = self.document
        _roles = self.roles

        if not _roles:
            log.debug("No roles to render.")
            return

        log.debug("Rendering roles section.")

        _doc.add_header("## Roles")

        for role in _roles:
            self.render_role(role)


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

        assert isinstance(
            document,
            MarkdownDoc,
        ), "document must be an instance of MarkdownDoc"
        assert isinstance(
            jinja_env,
            Environment,
        ), "jinja_env must be an instance of Environment"
        assert isinstance(
            projects,
            Projects,
        ), "projects must be an instance of Projects"
        assert isinstance(
            settings,
            ResumeProjectsSettings,
        ), "settings must be an instance of ResumeProjectsSettings"

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
            _doc.add_text(f"Url: {project.overview.url}")
        if _settings.url_description and project.overview.url_description:
            _doc.add_text(f"Url Description: {project.overview.url_description}")
        if _settings.start_date and project.overview.start_date:
            _doc.add_text(f"Start Date: {format_date(project.overview.start_date)}")
        if _settings.end_date and project.overview.end_date:
            _doc.add_text(f"End Date: {format_date(project.overview.end_date)}")

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
