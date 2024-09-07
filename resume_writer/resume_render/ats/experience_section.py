import logging
from datetime import datetime

import docx.document
from docx.shared import Pt

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
from resume_writer.resume_render.resume_render_base import (
    ResumeRenderExperienceBase,
    ResumeRenderProjectBase,
    ResumeRenderProjectsBase,
    ResumeRenderRoleBase,
    ResumeRenderRolesBase,
)

log = logging.getLogger(__name__)


class RenderRoleSection(ResumeRenderRoleBase):
    """Render experience roles section."""

    def __init__(
        self,
        document: docx.document.Document,
        role: Role,
        settings: ResumeRolesSettings,
    ):
        """Initialize roles render object."""

        log.debug("Initializing roles render object.")
        super().__init__(document=document, role=role, settings=settings)

    def _skills(self) -> list[str]:
        """Render role skills section."""

        log.debug("Rendering role skills.")
        _paragraph_lines = []
        if self.role.skills and self.settings.skills and len(self.role.skills) > 0:
            _skills_str = ", ".join(self.role.skills)
            _paragraph_lines.append(f"Skills: {_skills_str}")

        return _paragraph_lines

    def _details(self) -> list[str]:
        """Render role details section."""
        log.debug("Rendering role details.")
        _paragraph_lines = []
        # job category
        _basics = self.role.basics
        if _basics.job_category and self.settings.job_category:
            _paragraph_lines.append(f"{_basics.job_category}")

        if _basics.location and self.settings.location:
            _paragraph_lines.append(f"{_basics.location}")

        if _basics.agency_name and self.settings.agency_name:
            _paragraph_lines.append(f"{_basics.agency_name}")

        if _basics.employment_type and self.settings.employment_type:
            _paragraph_lines.append(f"{_basics.employment_type}")

        return _paragraph_lines

    def _dates(self) -> str:
        """Generate dates string for role."""

        log.debug("Rendering role dates.")

        _basics = self.role.basics
        # Start date
        if not _basics.start_date:
            _msg = "Start date is required"
            self.errors.append(_msg)
            log.warning(_msg)

        _value = datetime.strftime(_basics.start_date, "%m-%Y")
        _start_and_end = f"{_value}"

        # End date
        if _basics.end_date:
            _value = datetime.strftime(_basics.end_date, "%m-%Y")
            _start_and_end += f" - {_value}"
        else:
            _start_and_end += " - Present"

        return _start_and_end

    def render(self) -> None:
        """Render role overview/basics section."""

        _paragraph_lines = []

        _basics_paragraph = self.document.add_paragraph()

        log.debug("Rendering roles section.")
        _basics = self.role.basics

        # Add the company name
        # company name is required
        if not _basics.company:
            _msg = "Company name is required"
            self.errors.append(_msg)
            log.error(_msg)

        _company_run = _basics_paragraph.add_run(f"{_basics.company}")
        _company_run.bold = True
        _company_run.underline = True
        _company_run.font.size = Pt(self.font_size + 2)

        # move to next line
        _basics_paragraph.add_run().add_break()

        # Add the title
        if not _basics.title:
            _msg = "Title is required"
            self.errors.append(_msg)
            log.error(_msg)

        _title_run = _basics_paragraph.add_run(f"{_basics.title}")
        _title_run.bold = True

        # move to next line
        _basics_paragraph.add_run().add_break()

        # add the dates
        _date_line = self._dates()
        _basics_paragraph.add_run(f"{_date_line}")

        # add the details section such as job category, agency, etc.
        _details_paragraph = self.document.add_paragraph()

        _detail_lines = self._details()
        if len(_detail_lines) > 0:
            _paragraph_lines.extend(_detail_lines)

        _clean_lines = [_line.replace("\n\n", "\n") for _line in _paragraph_lines]

        if len(_paragraph_lines) > 0:
            _details_paragraph.add_run("\n".join(_clean_lines))

        # add the summary section
        if self.role.summary and self.settings.summary:
            _summary_paragraph = self.document.add_paragraph()
            _summary_paragraph.paragraph_format.space_after = Pt(self.font_size / 2)
            _summary_paragraph.paragraph_format.space_before = Pt(self.font_size / 2)
            _summary_run = _summary_paragraph.add_run(self.role.summary.text)
            _summary_run.italic = True

        # add the responsibilities section
        if self.role.responsibilities and self.settings.responsibilities:
            _responsibilities_text = self.role.responsibilities.text.replace(
                "\n\n",
                "\n",
            )
            _responsibilites_paragraph = self.document.add_paragraph()
            _responsibilities_run = _responsibilites_paragraph.add_run(
                _responsibilities_text,
            )
            _responsibilites_paragraph.paragraph_format.space_after = Pt(
                self.font_size / 2,
            )
            _responsibilites_paragraph.paragraph_format.space_before = Pt(
                self.font_size / 2,
            )

        _skills_lines = self._skills()
        if len(_skills_lines) > 0:
            _skills_paragraph = self.document.add_paragraph()
            _skills_paragraph.add_run("\n".join(_skills_lines))


class RenderRolesSection(ResumeRenderRolesBase):
    """Render experience roles section."""

    def __init__(
        self,
        document: docx.document.Document,
        roles: Roles,
        settings: ResumeRolesSettings,
    ):
        """Initialize roles render object."""

        super().__init__(document=document, roles=roles, settings=settings)

    def render(self) -> None:
        """Render roles section."""
        log.debug("Rendering roles section.")
        if len(self.roles) > 0:
            self.document.add_heading("Work History", level=2)
        else:
            log.info("No roles found")
            return

        for _role in self.roles:
            RenderRoleSection(
                document=self.document,
                role=_role,
                settings=self.settings,
            ).render()

            # add two blank lines between roles
            if _role != self.roles[-1]:
                self.document.add_paragraph()
                self.document.add_paragraph()


class RenderProjectSection(ResumeRenderProjectBase):
    """Render experience project section."""

    def __init__(
        self,
        document: docx.document.Document,
        project: Project,
        settings: ResumeProjectsSettings,
    ):
        """Initialize project render object."""
        log.debug("Initializing project render object.")
        super().__init__(document=document, project=project, settings=settings)

    def _overview(self) -> list[str]:
        """Render project overview section."""

        log.debug("Rendering project overview.")

        _paragraph_lines = []
        _overview = self.project.overview

        _url_line = ""
        if self.settings.url_description and _overview.url_description:
            _url_line = f"{_overview.url_description} "
        if self.settings.url and _overview.url:
            _url_line += f" ({_overview.url})"

        _url_line = _url_line.strip()
        if _url_line:
            _paragraph_lines.append(_url_line)

        if self.settings.start_date and _overview.start_date:
            _start_date = datetime.strftime(_overview.start_date, "%B %Y")
            _paragraph_lines.append(f"Start Date: {_start_date}")

        if self.settings.end_date and _overview.end_date:
            _end_date = datetime.strftime(_overview.end_date, "%B %Y")
            _paragraph_lines.append(f"End Date: {_end_date}")

        return _paragraph_lines

    def _skills(self) -> list[str]:
        """Render project skills section."""

        log.debug("Rendering project skills.")

        _paragraph_lines = []

        _skills = ", ".join(self.project.skills)
        _paragraph_lines.append(f"Skills: {_skills}")

        return _paragraph_lines

    def render(self) -> None:
        """Render project section."""

        log.debug("Rendering project section.")

        _paragraph_lines = []

        if self.settings.overview and self.project.overview:
            _paragraph_lines.extend(self._overview())

        if self.settings.description and self.project.description:
            _paragraph_lines.append(self.project.description.text)

        if self.settings.skills and len(self.project.skills) > 0:
            _paragraph_lines.extend(self._skills())

        if len(_paragraph_lines) > 0:
            self.document.add_paragraph("\n".join(_paragraph_lines))


class RenderProjectsSection(ResumeRenderProjectsBase):
    """Render experience projects section."""

    def __init__(
        self,
        document: docx.document.Document,
        projects: Projects,
        settings: ResumeProjectsSettings,
    ):
        """Initialize projects render object."""

        log.debug("Initializing projects render object.")

        super().__init__(document=document, projects=projects, settings=settings)

    def render(self) -> None:
        """Render projects section."""

        log.debug("Rendering projects section.")
        if len(self.projects) > 0:
            self.document.add_heading("Projects", level=2)
        for _project in self.projects:
            _project_render = RenderProjectSection(
                document=self.document,
                project=_project,
                settings=self.settings,
            ).render()


class RenderExperienceSection(ResumeRenderExperienceBase):
    """Render experience section."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeExperienceSettings,
    ) -> None:
        """Initialize experience render object."""

        log.debug("Initializing experience render object.")
        super().__init__(document=document, experience=experience, settings=settings)

    def render(self) -> None:
        """Render experience section."""

        log.debug("Rendering experience section.")

        if self.settings.roles and self.experience.roles:
            RenderRolesSection(
                document=self.document,
                roles=self.experience.roles,
                settings=self.settings.roles_settings,
            ).render()

        if self.settings.projects and self.experience.projects:
            RenderProjectsSection(
                document=self.document,
                projects=self.experience.projects,
                settings=self.settings.projects_settings,
            ).render()
