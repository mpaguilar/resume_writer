import logging
from datetime import datetime

import docx.document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Inches

from resume_writer.models.experience import (
    Experience,
)
from resume_writer.resume_render.render_settings import (
    ResumeSkillsMatrixSettings,
)
from resume_writer.resume_render.resume_render_base import (
    ResumeRenderSkillsMatrixBase,
)
from resume_writer.resume_render.skills_matrix import SkillsMatrix

log = logging.getLogger(__name__)


class RenderSkillsMatrixSection(ResumeRenderSkillsMatrixBase):
    """Render skills for a functional resume."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeSkillsMatrixSettings,
    ):
        """Initialize skills render object."""
        log.debug("Initializing functional skills render object.")
        super().__init__(document=document, experience=experience, settings=settings)

    def find_skill_date_range(
        self,
        skill: str,
    ) -> tuple[datetime | None, datetime | None]:
        """Find the earliest job with a skill."""

        _earliest_start_date = None
        _last_end_date = None

        # collect the start dates for each role with this skill
        _start_dates = [
            role.basics.start_date
            for role in self.experience.roles
            if skill in role.skills
        ]
        # collect the end dates for each role with this skill
        _end_dates = [
            role.basics.end_date
            for role in self.experience.roles
            if skill in role.skills
        ]

        # find the earliest start date
        if len(_start_dates) > 0:
            _earliest_start_date = min(_start_dates)
            _last_end_date = max(_end_dates)

        return _earliest_start_date, _last_end_date

    def _get_skills_matrix(self) -> dict[str, float]:
        """Get a matrix of skills and their years of experience."""
        _roles = self.experience.roles

        # use only skills specified in the settings
        _settings_skills = self.settings.skills

        # remove blank lines from skills
        _settings_skills = [x for x in _settings_skills if x]

        # get a dict of all skills and yoe
        _skills_matrix = SkillsMatrix(_roles)
        _all_skills_yoe = _skills_matrix.skills_experience()

        _skills_yoe = {}
        # filter out skills not in the settings
        for _setting_skill in _settings_skills:
            _skills_yoe[_setting_skill] = _all_skills_yoe.get(_setting_skill, 0.0)


        # sort skills by yoe
        _skills_yoe = dict(
            sorted(_skills_yoe.items(), key=lambda item: item[1], reverse=True),
        )
        return _skills_yoe

    def render(self) -> None:
        """Render skills section for functional resume."""

        log.debug("Rendering functional skills section.")

        if not self.experience.roles:
            raise ValueError("Experience must have roles for an executive summary.")

        _skills_yoe = self._get_skills_matrix()

        assert _skills_yoe is not None
        assert all(isinstance(x, str) for x in _skills_yoe)
        assert all(isinstance(x, float) for x in _skills_yoe.values())

        _num_rows = len(_skills_yoe) / 2
        _num_rows = int(_num_rows) + 1 if _num_rows % 1 > 0 else int(_num_rows)

        _skills_yoe_items = list(_skills_yoe.items())

        _table = self.document.add_table(rows=_num_rows, cols=4, style="Table Grid")

        # TODO: This will not scale with the font as-is
        _row_size = Inches(0.2)

        for x in range(_num_rows):
            _table.rows[x].height = _row_size

            # years of OTJ experience
            _cell1 = _table.cell(x, 0)
            _cell1.text = _skills_yoe_items[x][0]
            _cell1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            _cell2_text = str(_skills_yoe_items[x][1])
            _first_date, _last_date = self.find_skill_date_range(
                _skills_yoe_items[x][0],
            )

            # add first and last used dates
            _first_date_str = _first_date.strftime("%Y") if _first_date else "N/A"
            _last_date_str = _last_date.strftime("%Y") if _last_date else "N/A"

            _cell2_text = _cell2_text + f" / ({_first_date_str} - {_last_date_str})"

            _cell2 = _table.cell(x, 1)
            _cell2.text = str(_cell2_text)
            _cell2.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        for x in range(_num_rows, len(_skills_yoe_items)):
            # add skill name to first column
            _cell1 = _table.cell(x - _num_rows, 2)
            _cell1.text = _skills_yoe_items[x][0]
            _cell1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            _cell2_text = str(_skills_yoe_items[x][1])

            _first_date, _last_date = self.find_skill_date_range(
                _skills_yoe_items[x][0],
            )

            _first_date_str = _first_date.strftime("%Y") if _first_date else "N/A"
            _last_date_str = _last_date.strftime("%Y") if _last_date else "N/A"
            _cell2_text = _cell2_text + f"  / ({_first_date_str} - {_last_date_str})"

            _cell2 = _table.cell(x - _num_rows, 3)
            _cell2.text = _cell2_text
            _cell2.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        _table.autofit = True
