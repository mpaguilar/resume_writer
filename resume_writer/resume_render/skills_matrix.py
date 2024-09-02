import logging

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
        _skills_list = skills_list(self.roles)
        # for each skill, get the years of experience
        for skill in _skills_list:
            _skills[skill] = skill_experience(self.roles, skill)

        # remove skills with 0 years of experience
        _skills = {k: v for k, v in _skills.items() if v > 0}

        return _skills


def career_experience_total(roles: Roles) -> float:
    """Return statistics about job experience."""
    assert isinstance(roles, Roles)
    assert all(isinstance(role, Role) for role in roles)

    _date_stats = DateStats()
    for role in roles:
        _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

    _yoe = _date_stats.years_of_experience

    return _yoe


def career_experience_span(roles: Roles) -> float:
    """Return years from first used to last."""

    assert isinstance(roles, Roles)
    assert all(isinstance(role, Role) for role in roles)

    _date_stats = DateStats()
    for role in roles:
        _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)
    _yoe = _date_stats.span_of_experience

    return _yoe


def skills_list(roles: Roles) -> list:
    """Return a list of unique skills."""

    assert isinstance(roles, Roles)

    _skills = []

    for role in roles:
        for skill in role.skills:
            if skill not in _skills:
                _skills.append(skill)

    return _skills


def skill_experience(roles: Roles, skill: str) -> float:
    """Return years of experience with a skill."""
    assert isinstance(roles, Roles)

    _date_stats = DateStats()
    for role in roles:
        if skill in role.skills:
            _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

    return _date_stats.years_of_experience


def skills_experience(roles: Roles) -> dict:
    """Return a dictionary of skills and years of experience."""

    assert isinstance(roles, Roles)

    _skills = {}

    # get a list of unique skills
    _skills_list = skills_list(roles)
    # for each skill, get the years of experience
    for skill in _skills_list:
        _skills[skill] = skill_experience(roles, skill)

    # remove skills with 0 years of experience
    _skills = {k: v for k, v in _skills.items() if v > 0}

    return _skills
