import logging
from datetime import datetime

from resume_writer.models.experience import Role, Roles
from resume_writer.utils.resume_stats import DateStats

log = logging.getLogger(__name__)


class SkillsMatrix:
    """A matrix of skills, includes years and spans of experience.

    Attributes:
        roles (Roles): A collection of Role objects representing the user's work experience.

    Notes:
        1. The class processes skill data from roles to calculate experience metrics.
        2. It supports calculating total career experience, span of experience, and skill-specific metrics.
        3. The matrix can filter skills based on a provided list or include all skills if "*all*" is specified.
        4. The matrix includes years of experience and first/last usage dates for each skill.
        5. Results are sorted by years of experience in descending order.
    """

    def __init__(self, roles: Roles):
        """Initialize the matrix with a list of roles.

        Args:
            roles (Roles): A collection of Role objects representing the user's work experience.

        Raises:
            AssertionError: If roles is not an instance of Roles or if any role is not a Role instance.
        """
        assert isinstance(roles, Roles)
        assert all(isinstance(role, Role) for role in roles)
        self.roles = roles

    def career_experience_total(self) -> float:
        """Return the total years of career experience across all roles.

        Returns:
            float: The total years of experience calculated from all role date ranges.

        Notes:
            1. Creates a DateStats instance to manage date ranges.
            2. Iterates through each role and adds its start and end dates to the date stats.
            3. Returns the total years of experience from the date stats.
        """
        assert all(isinstance(role, Role) for role in self.roles)

        _date_stats = DateStats()
        for role in self.roles:
            _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

        _yoe = _date_stats.years_of_experience

        return _yoe

    def career_experience_span(self) -> float:
        """Return the span of career experience, from first to last role.

        Returns:
            float: The span of years between the earliest start date and latest end date.

        Notes:
            1. Creates a DateStats instance to manage date ranges.
            2. Iterates through each role and adds its start and end dates to the date stats.
            3. Returns the span of experience from the date stats.
        """
        assert all(isinstance(role, Role) for role in self.roles)

        _date_stats = DateStats()
        for role in self.roles:
            _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)
        _yoe = _date_stats.span_of_experience

        return _yoe

    def skills_list(self) -> list:
        """Return a list of unique skills from all roles.

        Returns:
            list: A list of unique skill strings found across all roles.

        Notes:
            1. Initializes an empty list to store unique skills.
            2. Iterates through each role and adds each skill to the list if not already present.
            3. Returns the list of unique skills.
        """
        _skills = []

        for role in self.roles:
            if role.skills:
                for skill in role.skills:
                    if skill not in _skills:
                        _skills.append(skill)

        return _skills

    def skill_experience(self, skill: str) -> float:
        """Return the total years of experience with a specific skill.

        Args:
            skill (str): The name of the skill to evaluate.

        Returns:
            float: The total years of experience with the skill across all roles.

        Notes:
            1. Creates a DateStats instance to track date ranges for the skill.
            2. Iterates through each role and checks if the skill is present.
            3. If the skill is found, adds the role's date range to the date stats.
            4. Returns the total years of experience from the date stats.
        """
        _date_stats = DateStats()
        for role in self.roles:
            if skill in role.skills:
                _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

        return _date_stats.years_of_experience

    def skills_experience(self) -> dict:
        """Return a dictionary mapping each skill to its years of experience.

        Returns:
            dict: A dictionary where keys are skill names and values are float years of experience.

        Notes:
            1. Retrieves the list of unique skills using skills_list.
            2. For each skill, calculates its years of experience using skill_experience.
            3. Filters out skills with zero experience.
            4. Returns the resulting dictionary with only non-zero experience entries.
        """
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
        """Return a dictionary of skills with years of experience and usage dates.

        Args:
            skills (list[str]): List of skills to include. If "*all*" is provided, all skills are included.

        Returns:
            dict: A dictionary where each key is a skill name and the value is a dict with:
                - "yoe" (float): Years of experience with the skill.
                - "first_used" (datetime | None): Earliest date the skill was used.
                - "last_used" (datetime | None): Latest date the skill was used.

        Raises:
            AssertionError: If skills is not a list or if any element is not a string.

        Notes:
            1. Validates input to ensure skills is a list of strings.
            2. Retrieves the full list of unique skills from the resume.
            3. If the skills list is ["*all*"], uses all skills; otherwise, filters to only those present.
            4. Removes empty strings and skills not found in the resume.
            5. Returns an empty dict if no valid skills are found.
            6. For each valid skill, retrieves years of experience and first/last usage dates.
            7. Constructs the result dictionary with skill data.
            8. Sorts the result by years of experience in descending order.
            9. No external I/O (network, disk, or database) is performed.
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
        """Return the first and last usage dates for a specific skill.

        Args:
            skill (str): The name of the skill to evaluate.

        Returns:
            tuple[datetime | None, datetime | None]: A tuple containing:
                - The earliest start date the skill was used, or None if not used.
                - The latest end date the skill was used, or None if not used.

        Notes:
            1. Initializes variables to track the earliest start and latest end dates.
            2. Collects all start dates from roles where the skill is present.
            3. Collects all end dates from roles where the skill is present.
            4. If any start dates exist, finds the earliest and latest end date.
            5. Returns the earliest and latest dates as a tuple.
            6. No external I/O (network, disk, or database) is performed.
        """
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
