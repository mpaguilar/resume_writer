import logging

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
    """Render experience roles section.

    This class is responsible for rendering individual roles within the experience section of a resume.
    It inherits from ResumeRenderRolesBase, which provides base functionality for rendering role-related content.

    Attributes:
        document (MarkdownDoc): The MarkdownDoc object to render the content into.
        roles (Roles): The list of Role objects to render.
        settings (ResumeRolesSettings): The settings object controlling what fields to render.
    """

    def __init__(
        self,
        document: MarkdownDoc,
        roles: Roles,
        settings: ResumeRolesSettings,
    ):
        """Initialize roles render object.

        Args:
            document (MarkdownDoc): The MarkdownDoc object to render the content into.
            roles (Roles): The list of Role objects to render.
            settings (ResumeRolesSettings): The settings object controlling what fields to render.

        Returns:
            None

        Notes:
            1. Validate that `document` is an instance of MarkdownDoc.
            2. Validate that `roles` is an instance of Roles.
            3. Validate that `settings` is an instance of ResumeRolesSettings.
            4. Call the parent class constructor with the provided arguments.

        """
        assert isinstance(
            document,
            MarkdownDoc,
        ), "document should be an instance of MarkdownDoc"
        assert isinstance(roles, Roles), "roles should be an instance of Roles"
        assert isinstance(
            settings,
            ResumeRolesSettings,
        ), "settings should be an instance of ResumeRolesSettings"

        super().__init__(
            document=document,
            jinja_env=None,
            roles=roles,
            template_name="",
            settings=settings,
        )

    def render_basics(self, role: Role) -> None:
        """Render role basics.

        Args:
            role (Role): The Role object containing the basic information to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. Add a header for the basics section.
            3. Render the company name if present.
            4. Render the agency name if the setting is enabled and the field is present.
            5. Render the job category if the setting is enabled and the field is present.
            6. Render the employment type if the setting is enabled and the field is present.
            7. Render the start date if the setting is enabled and the field is present.
            8. Render the end date if the setting is enabled and the field is present.
            9. Render the title if present.
            10. Render the reason for change if the setting is enabled and the field is present.
            11. Render the location if the setting is enabled and the field is present.

        """
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
        """Render role highlights.

        Args:
            role (Role): The Role object containing the highlights to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. If highlights are enabled in settings and the role has highlights, add a header for highlights.
            3. For each highlight in the role, add a bullet point to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.highlights and role.highlights:
            _doc.add_header("#### Highlights")
            for highlight in role.highlights:
                _doc.add_text(f"- {highlight}")

    def render_responsibilities(self, role: Role) -> None:
        """Render role responsibilities.

        Args:
            role (Role): The Role object containing the responsibilities to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. If responsibilities are enabled in settings and the role has responsibilities, add a header for responsibilities.
            3. For each responsibility in the role, add a bullet point to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.responsibilities and role.responsibilities:
            _doc.add_header("#### Responsibilities")
            for responsibility in role.responsibilities:
                _doc.add_text(f"- {responsibility}")

    def render_skills(self, role: Role) -> None:
        """Render role skills.

        Args:
            role (Role): The Role object containing the skills to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. If skills are enabled in settings and the role has skills, add a header for skills.
            3. For each skill in the role, add a bullet point to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.skills and role.skills:
            _doc.add_header("#### Skills")
            for skill in role.skills:
                _doc.add_text(f"- {skill}")

    def render_projects(self, role: Role) -> None:
        """Render role projects.

        Args:
            role (Role): The Role object containing the projects to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. If projects are enabled in settings and the role has projects, add a header for projects.
            3. For each project in the role, add a bullet point to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        if _settings.projects and role.projects:
            _doc.add_header("#### Projects")
            for project in role.projects:
                _doc.add_text(f"- {project}")

    def render_role(self, role: Role) -> None:
        """Render a single role.

        Args:
            role (Role): The Role object to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. Add a header for the role section.
            3. Render the role basics.
            4. If summary is enabled and the role has a non-empty summary, add a header and render the summary.
            5. If responsibilities are enabled and the role has a text field for responsibilities, add a header and render the text.
            6. If skills are enabled and the role has skills, add a header and render each skill with an asterisk bullet.

        """
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
        """Render roles section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and roles.
            2. If no roles are present, log a debug message and return.
            3. Log a debug message indicating that rendering is starting.
            4. Add a header for the roles section.
            5. For each role in the roles list, render the role.

        """
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
    """Render experience projects section.

    This class is responsible for rendering individual projects within the experience section of a resume.
    It inherits from ResumeRenderProjectsBase, which provides base functionality for rendering project-related content.

    Attributes:
        document (MarkdownDoc): The MarkdownDoc object to render the content into.
        projects (Projects): The list of Project objects to render.
        settings (ResumeProjectsSettings): The settings object controlling what fields to render.
    """

    def __init__(
        self,
        document: MarkdownDoc,
        projects: Projects,
        settings: ResumeProjectsSettings,
    ):
        """Initialize projects render object.

        Args:
            document (MarkdownDoc): The MarkdownDoc object to render the content into.
            projects (Projects): The list of Project objects to render.
            settings (ResumeProjectsSettings): The settings object controlling what fields to render.

        Returns:
            None

        Notes:
            1. Log a debug message indicating initialization.
            2. Validate that `document` is an instance of MarkdownDoc.
            3. Validate that `projects` is an instance of Projects.
            4. Validate that `settings` is an instance of ResumeProjectsSettings.
            5. Call the parent class constructor with the provided arguments.

        """
        log.debug("Initializing projects render object.")

        assert isinstance(
            document,
            MarkdownDoc,
        ), "document must be an instance of MarkdownDoc"
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
            jinja_env=None,
            projects=projects,
            template_name="",
            settings=settings,
        )

    def render_project(self, project: Project) -> None:
        """Render a single project.

        Args:
            project (Project): The Project object to render.

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document and settings.
            2. Add a header for the project section.
            3. Add a header for the overview section.
            4. Render the project title if enabled in settings and present.
            5. Render the project URL if enabled in settings and present.
            6. Render the URL description if enabled in settings and present.
            7. Render the start date if enabled in settings and present.
            8. Render the end date if enabled in settings and present.
            9. If a description is enabled in settings and present, add a header and render the description.
            10. If skills are enabled in settings and present, add a header and render each skill with an asterisk bullet.

        """
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
        """Render projects section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Extract shortcuts for the document, settings, and projects.
            2. If no projects are present, log a debug message and return.
            3. Log a debug message indicating that rendering is starting.
            4. Add a header for the projects section.
            5. For each project in the projects list, render the project.

        """
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
    """Render experience section.

    This class is responsible for orchestrating the rendering of both roles and projects within the experience section of a resume.
    It inherits from ResumeRenderExperienceBase, which provides base functionality for rendering experience-related content.

    Attributes:
        document (MarkdownDoc): The MarkdownDoc object to render the content into.
        experience (Experience): The Experience object containing the data to render.
        settings (ResumeExperienceSettings): The settings object controlling what fields to render.
    """

    def __init__(
        self,
        document: MarkdownDoc,
        experience: Experience,
        settings: ResumeExperienceSettings,
    ) -> None:
        """Initialize experience render object.

        Args:
            document (MarkdownDoc): The MarkdownDoc object to render the content into.
            experience (Experience): The Experience object containing the data to render.
            settings (ResumeExperienceSettings): The settings object controlling what fields to render.

        Returns:
            None

        Notes:
            1. Log a debug message indicating initialization.
            2. Call the parent class constructor with the provided arguments.

        """
        log.debug("Initializing experience render object.")
        super().__init__(
            document=document,
            jinja_env=None,
            experience=experience,
            settings=settings,
        )

    def render(self) -> None:
        """Render experience section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Log a debug message indicating that rendering is starting.
            2. Add a header for the experience section.
            3. If projects are enabled in settings and the experience has projects, render the projects section.
            4. If roles are enabled in settings and the experience has roles, render the roles section.

        """
        log.debug("Rendering experience section.")

        self.document.add_header("# Experience")

        if self.settings.projects and self.experience.projects:
            RenderProjectsSection(
                document=self.document,
                projects=self.experience.projects,
                settings=self.settings.projects_settings,
            ).render()

        if self.settings.roles and self.experience.roles:
            RenderRolesSection(
                document=self.document,
                roles=self.experience.roles,
                settings=self.settings.roles_settings,
            ).render()
