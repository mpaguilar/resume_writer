import logging
import re
from datetime import datetime

import docx
import docx.document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches, Pt

from resume_writer.models.experience import (
    Experience,
    Project,
    Projects,
    Role,
    Roles,
)
from resume_writer.resume_render.docx_hyperlink import add_hyperlink
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
from resume_writer.utils.skills_splitter import skills_splitter

log = logging.getLogger(__name__)

_punctuation_end_re = re.compile(r"[\).,!?;:\]]")


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

        _paragraph = self.document.add_paragraph()

        if self.role.skills and self.settings.skills and len(self.role.skills) > 0:
            _skills_str = ", ".join(self.role.skills)
            _skills_run = _paragraph.add_run(f"Skills: {_skills_str}")
            _skills_run.font.size = Pt(self.font_size - 2)
            _skills_run.font.italic = True

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
        _title_run.font.size = Pt(self.font_size + 2)

        # company name is required
        if not _basics.company:
            _msg = "Company name is required"
            self.errors.append(_msg)
            log.error(_msg)
            raise ValueError(_msg)

        _company_run = paragraph.add_run(f"\t{_basics.company}")
        _company_run.bold = True
        _company_run.font.size = Pt(self.font_size + 2)

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
            _date_run.add_text(f" - {_value}")
        else:
            _date_run.add_text(" - Present")

        if _basics.location and self.settings.location:
            paragraph.add_run(f"\t{_basics.location}")

    def _render_task(
        self,
        paragraph: docx.text.paragraph.Paragraph,
        task_line: str,
    ) -> None:
        if (
            self.role.skills
            and self.settings.include_tasks
            and len(self.role.skills) > 0
        ):
            _fragments = skills_splitter(task_line, self.role.skills)
            _leading_space = True
            _trailing_space = True
            for _ndx, _fragment in enumerate(_fragments):
                _run = paragraph.add_run()

                if (_ndx + 1) < len(_fragments) and not _punctuation_end_re.match(
                        _fragments[_ndx + 1],
                    ):
                    _trailing_space = True
                else:
                    _trailing_space = False

                if _fragment in self.role.skills:
                    if _leading_space:
                        _run.add_text(" ")

                    _run.add_text(_fragment)
                    _run.bold = True

                    if _trailing_space:
                        _run.add_text(" ")
                else:
                    _run.add_text(_fragment)

                # used on the next iteration of the loop
                _leading_space = not re.search(r"[({[]$", _fragment)

            _run.add_break()

    def _responsibilities(self) -> None:
        _msg = f"Rendering responsibilities for role {self.role.basics.title}"
        log.debug(_msg)

        _situation_paragraph = self.document.add_paragraph()
        _situation_paragraph.paragraph_format.space_before = Pt(0)
        _situation_paragraph.paragraph_format.space_after = Pt(6)

        _tasks_paragraph = self.document.add_paragraph()
        _tasks_paragraph.paragraph_format.space_before = Pt(0)
        _tasks_paragraph.paragraph_format.space_after = Pt(6)

        _responsibilities_lines: list[str] = self.role.responsibilities.text.replace(
            "\n\n",
            "\n",
        ).split("\n")

        for _line in _responsibilities_lines:
            # task lines start with "* "
            if _line.startswith("* ") and self.settings.include_tasks:
                self._render_task(_tasks_paragraph, _line)

            if self.settings.include_situation and _line and not _line.startswith("* "):
                _situation_run = _situation_paragraph.add_run()
                _situation_run.add_text(_line)
                _situation_run.add_break()

    def _description(self) -> None:
        """Render role summary and details section."""

        if self.role.summary and self.settings.summary:
            _summary_paragraph = self.document.add_paragraph()
            _summary_run = _summary_paragraph.add_run()
            _summary_run.add_text(self.role.summary.summary.strip())
            _summary_run.font.italic = True
            _summary_run.font.bold = True
            _summary_paragraph.paragraph_format.space_after = Pt(self.font_size)
            _summary_paragraph.paragraph_format.space_before = Pt(0)

        if self.role.responsibilities and self.settings.responsibilities:
            self._responsibilities()

    def render(self) -> None:
        """Render role overview/basics section."""

        log.debug("Rendering roles section.")

        _basics_paragraph = self.document.add_paragraph()
        _basics_paragraph.paragraph_format.space_after = Pt(self.font_size / 2)
        self._title_and_company(_basics_paragraph)

        # add tab stops to format title, company, dates, and location neatly
        _tab_stop_right = Inches(7.4)
        _tab_stops = _basics_paragraph.paragraph_format.tab_stops

        _tab_stops.add_tab_stop(
            _tab_stop_right,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.SPACES,
        )

        _dates_paragraph = self.document.add_paragraph()
        # add tab stops to format title, company, dates, and location neatly
        _tab_stop_right = Inches(7.4)
        _tab_stops = _dates_paragraph.paragraph_format.tab_stops

        _tab_stops.add_tab_stop(
            _tab_stop_right,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.SPACES,
        )

        self._dates_and_location(_dates_paragraph)
        _dates_paragraph.paragraph_format.space_after = Pt(self.font_size / 2)

        self._description()
        self._skills()


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

    def _overview(self, paragraph: docx.text.paragraph.Paragraph) -> None:
        """Render project overview section."""

        log.debug("Rendering project overview.")

        _overview = self.project.overview

        _title_run = paragraph.add_run()
        _title_run.add_text(_overview.title)
        _title_run.bold = True

        paragraph.add_run("\t")
        paragraph.paragraph_format.space_after = Pt(6)

        add_hyperlink(paragraph, f"Website: {_overview.url_description}", _overview.url)

    def _skills(self, paragraph: docx.text.paragraph.Paragraph) -> list[str]:
        """Render project skills section."""

        log.debug("Rendering project skills.")

        _skills = ", ".join(self.project.skills)
        _skills_run = paragraph.add_run()

        _skills_run.add_text(f"Skills: {_skills}")
        _skills_run.italic = True

    def render(self) -> None:
        """Render project section."""

        log.debug("Rendering project section.")

        _paragraph = self.document.add_paragraph()
        # add tab stops to format title, company, dates, and location neatly
        _tab_stop_right = Inches(7.4)
        _tab_stops = _paragraph.paragraph_format.tab_stops

        _tab_stops.add_tab_stop(
            _tab_stop_right,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.SPACES,
        )

        if self.settings.overview and self.project.overview:
            self._overview(_paragraph)

        _paragraph.paragraph_format.space_after = Pt(6)

        if self.settings.description and self.project.description:
            _description_paragraph = self.document.add_paragraph()
            _description_run = _description_paragraph.add_run()
            _description_lines = self.project.description.text.split("\n")
            for _line in _description_lines:
                _line = _line.strip()
                if _line:
                    _description_run.add_text(_line)
                    _description_run.add_break()

            _description_paragraph.paragraph_format.space_before = Pt(0)
            _description_paragraph.paragraph_format.space_after = Pt(0)

        if self.settings.skills and self.project.skills:
            _skills_paragraph = self.document.add_paragraph()
            self._skills(_skills_paragraph)
            _skills_paragraph.paragraph_format.space_before = Pt(0)
            _skills_paragraph.paragraph_format.space_after = Pt(6)


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
