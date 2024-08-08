import logging
from datetime import datetime
from typing import TypeVar

from resume_writer.models.parsers import (
    BasicBlockParse,
    LabelBlockParse,
    ListBlockParse,
    MultiBlockParse,
    ParseError,
    TextBlockParse,
)

T = TypeVar("T")


log = logging.getLogger(__name__)


class ParseRoleError(ParseError):
    """Error parsing a role."""


class RoleSummary(TextBlockParse):
    """Brief description of a role."""

    def __init__(self, summary: str):
        """Initialize the object."""
        assert isinstance(summary, str), "Summary must be a string"
        self.summary = summary


class RoleResponsibilities(TextBlockParse):
    """Detailed description of role responsibilities."""

    def __init__(self, responsibilities: str):
        """Initialize the object."""

        if not isinstance(responsibilities, str):
            raise ParseRoleError("Responsibilities must be a string")
        self.text = responsibilities


class RoleSkills(ListBlockParse):
    """Skills used in a role."""

    def __init__(self, skills: list[str]) -> None:
        """Initialize the object."""
        assert isinstance(skills, list), "Skills must be a list"
        assert all(isinstance(skill, str) for skill in skills), "Skills must be strings"
        self.skills = skills

    def __iter__(self):
        """Iterate over the skills."""
        return iter(self.skills)

    def __len__(self):
        """Return the number of skills."""
        return len(self.skills)

    def __getitem__(self, index: int):
        """Return the skill at the given index."""
        return self.skills[index]


class RoleBasics(LabelBlockParse):
    """Relevant basics for a resume."""

    def __init__( #noqa: PLR0913
        self,
        company: str,
        start_date: str | datetime,
        end_date: str | datetime | None,
        reason_for_change: str | None,
        title: str,
        location: str | None = None,
        job_category : str | None = None,
        employment_type : str | None = None,
        agency_name : str | None = None,

    ):
        """Initialize the object."""

        if not isinstance(company, str):
            raise ParseRoleError("Company name must be a string")

        if not isinstance(title, str):
            raise ParseRoleError("Job title must be a string")

        assert isinstance(
            start_date,
            (datetime | str),
        ), "Start date must be a datetime object or string"

        assert isinstance(end_date, (datetime, str, type(None)))
        assert isinstance(reason_for_change, (str, type(None)))
        assert isinstance(location, (str, type(None)))
        assert isinstance(job_category, (str, type(None)))
        assert isinstance(employment_type, (str, type(None)))
        assert isinstance(agency_name, (str, type(None)))

        self.company = company
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%m/%Y")  # noqa: DTZ007
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%m/%Y")  # noqa: DTZ007
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.reason_for_change = reason_for_change
        self.location = location
        self.job_category = job_category
        self.employment_type = employment_type
        self.agency_name = agency_name

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "company": "company",
            "start date": "start_date",
            "end date": "end_date",
            "reason for change": "reason_for_change",
            "title": "title",
            "location": "location",
            "job category": "job_category",
            "employment type": "employment_type",
            "agency": "agency_name",
        }


class Role(BasicBlockParse):
    """Details of a single work-related experience."""

    def __init__(
        self,
        basics: RoleBasics | None,
        summary: RoleSummary | None,
        responsibilities: RoleResponsibilities | None,
        skills: RoleSkills | None,
    ):
        """Initialize the object."""
        assert isinstance(
            basics,
            (RoleBasics, type(None)),
        ), "Basics must be a RoleBasics object or None"
        assert isinstance(
            summary,
            (RoleSummary, type(None)),
        ), "Summary must be a RoleSummary object or None"
        assert isinstance(
            responsibilities,
            (RoleResponsibilities, type(None)),
        ), "Responsibilities must be a RoleResponsibilities object or None"
        assert isinstance(
            skills,
            (RoleSkills, type(None)),
        ), "Skills must be a RoleSkills object or None"

        self.basics = basics
        self.summary = summary
        self.responsibilities = responsibilities
        self.skills = skills

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks for this object."""

        return {
            "basics": "basics",
            "summary": "summary",
            "responsibilities": "responsibilities",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks."""
        return {
            "basics": RoleBasics,
            "summary": RoleSummary,
            "responsibilities": RoleResponsibilities,
            "skills": RoleSkills,
        }


class Experience(MultiBlockParse):
    """Details of experience."""

    def __init__(
        self,
        experience: list[Role],
    ):
        """Initialize with a list of Role objects."""

        assert isinstance(experience, list), "Roles must be a list"
        assert all(
            isinstance(role, Role) for role in experience
        ), "Roles must be Role objects"

        log.info(f"Creating Roles object with {len(experience)} roles.")

        self.roles = experience

    def __iter__(self):
        """Iterate over the roles."""
        return iter(self.roles)

    def __len__(self):
        """Return the number of roles."""
        return len(self.roles)

    def __getitem__(self, index: int):
        """Return the role at the given index."""
        return self.roles[index]

    @staticmethod
    def list_class() -> type:
        """Return the class of the list items."""
        return Role
