import logging
from datetime import datetime

import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches, Pt
from resume_render.render_settings import (
    ResumeExperienceSettings,
    ResumeProjectsSettings,
    ResumeRolesSettings,
)
from resume_render.resume_render_base import (
    ResumeRenderExperienceBase,
    ResumeRenderProjectBase,
    ResumeRenderProjectsBase,
    ResumeRenderRoleBase,
    ResumeRenderRolesBase,
)

from resume_writer.models.experience import (
    Experience,
    Project,
    Projects,
    Role,
    Roles,
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
            _paragraph_lines.append(f"Job Category: {_basics.job_category}")

        if _basics.location and self.settings.location:
            _paragraph_lines.append(f"Location: {_basics.location}")

        if _basics.agency_name and self.settings.agency_name:
            _paragraph_lines.append(f"Agency: {_basics.agency_name}")

        if _basics.employment_type and self.settings.employment_type:
            _paragraph_lines.append(f"Employment Type: {_basics.employment_type}")

        return _paragraph_lines

    def _title_and_company(self, paragraph: docx.text.paragraph.Paragraph) -> None:
        """Render role title and company section."""

        log.debug("Rendering role title and company.")

        _basics = self.role.basics

        # title is required
        if not _basics.title:
            _msg = "Title is required"
            self.errors.append(_msg)
            log.error(_msg)
            raise ValueError(_msg)

        _title_run = paragraph.add_run()
        _title_run.add_text(f"{_basics.title}")
        _title_run.bold = True
        _title_run.underline = True
        _title_run.font.size = self.font_size + 2

        # company name is required
        if not _basics.company:
            _msg = "Company name is required"
            self.errors.append(_msg)
            log.error(_msg)
            raise ValueError(_msg)

        _company_run = paragraph.add_run(f"\t{_basics.company}")
        _company_run.bold = True
        _company_run.font.size = self.font_size + 2

        _company_run.add_break()

    def _dates_and_location(
        self,
        paragraph: docx.text.paragraph.Paragraph,
    ) -> list[str]:
        """Render role dates section."""

        log.debug("Rendering role dates.")

        _basics = self.role.basics

        _date_run = paragraph.add_run()

        # Start date
        if not _basics.start_date:
            _msg = "Start date is required"
            self.errors.append(_msg)
            log.warning(_msg)

        _value = datetime.strftime(_basics.start_date, "%B %Y")
        _date_run.add_text(f"{_value}")

        # End date
        if _basics.end_date:
            _value = datetime.strftime(_basics.end_date, "%B %Y")
            _date_run.add_text(f"- {_value}")
        else:
            _date_run.add_text(" - Present")

        if _basics.location and self.settings.location:
            paragraph.add_run(f"\t{_basics.location}")

    def _description(self, paragraph: docx.text.paragraph.Paragraph) -> None:
        """Render role summary and details section."""
        _run = paragraph.add_run()
        if self.role.summary and self.settings.summary:
            self.document.add_paragraph(self.role.summary.summary)

        if self.role.responsibilities and self.settings.responsibilities:
            self.document.add_paragraph(self.role.responsibilities.text)

    def render(self) -> None:
        """Render role overview/basics section."""

        log.debug("Rendering roles section.")

        _paragraph = self.document.add_paragraph()

        # add tab stops to format title, company, dates, and location neatly
        _tab_stop_right = Inches(7.4)
        _tab_stops = _paragraph.paragraph_format.tab_stops

        _tab_stops.add_tab_stop(
            _tab_stop_right,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.SPACES,
        )

        self._title_and_company(_paragraph)
        self._dates_and_location(_paragraph)

        _paragraph_lines = []
        _description_paragraph = self.document.add_paragraph()
        self._description(_description_paragraph)

        ###################
        _skills_lines = self._skills()
        if len(_skills_lines) > 0:
            _paragraph_lines.extend(_skills_lines)

        if len(_paragraph_lines) > 0:
            self.document.add_paragraph("\n".join(_paragraph_lines))


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
            _heading = self.document.add_heading("Work History", level=2)
            _heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            log.info("No roles found")
            return

        for _role in self.roles:
            RenderRoleSection(
                document=self.document,
                role=_role,
                settings=self.settings,
            ).render()

            _paragraph = self.document.add_paragraph()
            _paragraph.paragraph_format.space_after = Pt(12)

            self.add_horizontal_line(_paragraph, 2)


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
