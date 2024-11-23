import logging
from datetime import datetime

from resume_writer.models.experience import Role, Roles
from resume_writer.utils.resume_stats import DateStats

log = logging.getLogger(__name__)


class SkillsMatrix:
    """A matrix of skills, includes years and spans of experience."""

    def __init__(self, roles: Roles):
        """Initialize the matrix."""

        assert isinstance(roles, Roles)
        assert all(isinstance(role, Role) for role in roles)
        self.roles = roles

    def career_experience_total(self) -> float:
        """Return statistics about job experience."""
        assert all(isinstance(role, Role) for role in self.roles)

        _date_stats = DateStats()
        for role in self.roles:
            _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

        _yoe = _date_stats.years_of_experience

        return _yoe

    def career_experience_span(self) -> float:
        """Return years from first used to last."""

        assert all(isinstance(role, Role) for role in self.roles)

        _date_stats = DateStats()
        for role in self.roles:
            _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)
        _yoe = _date_stats.span_of_experience

        return _yoe

    def skills_list(self) -> list:
        """Return a list of unique skills."""

        _skills = []

        for role in self.roles:
            for skill in role.skills:
                if skill not in _skills:
                    _skills.append(skill)

        return _skills

    def skill_experience(self, skill: str) -> float:
        """Return years of experience with a skill."""

        _date_stats = DateStats()
        for role in self.roles:
            if skill in role.skills:
                _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

        return _date_stats.years_of_experience

    def skills_experience(self) -> dict:
        """Return a dictionary of skills and years of experience."""

        _skills = {}

        # get a list of unique skills
        _skills_list = self.skills_list()
        # for each skill, get the years of experience
        for skill in _skills_list:
            _skills[skill] = self.skill_experience(skill)

        # remove skills with 0 years of experience
        _skills = {k: v for k, v in _skills.items() if v > 0}

        return _skills

    def matrix(self, skills: list[str]) -> dict:
        """Return skills, years of experience, and when that skill was used.

        To retrieve all skills, send a single skill `*all*`.
        """

        assert isinstance(skills, list)
        assert all(isinstance(skill, str) for skill in skills)

        _all_skills = self.skills_list()

        if len(skills) == 1 and skills[0] == "*all*":
            _return_skills = _all_skills
        else:
            # remove blank lines from skills
            _return_skills = [x for x in skills if x.strip()]
            # remove skills that are not in the resume
            _return_skills = [x for x in _return_skills if x in _all_skills]

        # if no skills are found, return an empty dictionary
        if not _return_skills:
            return {}

        # create a matrix of skills and years of experience
        _skills_matrix = {}

        # get a list of all the skills and years of experience
        _all_skills_yoe = self.skills_experience()

        for _skill, _yoe in _all_skills_yoe.items():
            # only add skills that are in the list of skills to return
            if _skill not in _return_skills:
                continue

            # add the skill to the matrix
            _skills_matrix[_skill] = {}

            # add the years of experience to the matrix
            _skills_matrix[_skill]["yoe"] = _yoe

            # get the first and last usage of the skill
            _date_range = self.find_skill_date_range(_skill)
            _skills_matrix[_skill]["first_used"] = _date_range[0]
            _skills_matrix[_skill]["last_used"] = _date_range[1]

        _skills_matrix = dict(
            sorted(
                _skills_matrix.items(),
                key=lambda item: item[1]["yoe"],
                reverse=True,
            ),
        )

        return _skills_matrix

    def find_skill_date_range(
        self,
        skill: str,
    ) -> tuple[datetime | None, datetime | None]:
        """Return the first and last usage of a skill."""

        _earliest_start_date = None
        _last_end_date = None

        # collect the start dates for each role with this skill
        _start_dates = [
            role.basics.start_date for role in self.roles if skill in role.skills
        ]
        # collect the end dates for each role with this skill
        _end_dates = [
            role.basics.end_date for role in self.roles if skill in role.skills
        ]

        # find the earliest start date
        if len(_start_dates) > 0:
            _earliest_start_date = min(_start_dates)
            _last_end_date = max(_end_dates)

        # return the first and last usage of the skill
        return _earliest_start_date, _last_end_date
