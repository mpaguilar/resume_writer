import logging
from datetime import datetime
from typing import TypeVar

from resume_writer.models.parsers import (
    BasicBlockParse,
    LabelBlockParse,
    ListBlockParse,
    MultiBlockParse,
    TextBlockParse,
)

T = TypeVar("T")


log = logging.getLogger(__name__)


class RoleDescription(TextBlockParse):
    """Brief description of a role."""

    def __init__(self, description: str):
        """Initialize the object."""
        assert isinstance(description, str), "Description must be a string"
        self.description = description


class RoleResponsibilities(TextBlockParse):
    """Detailed description of role responsibilities."""

    def __init__(self, responsibilities: str):
        """Initialize the object."""
        assert isinstance(responsibilities, str), "Responsibilities must be a string"
        self.responsibilities = responsibilities


class RoleSkills(ListBlockParse):
    """Skills used in a role."""

    def __init__(self, skills: list[str]) -> None:
        """Initialize the object."""
        assert isinstance(skills, list), "Skills must be a list"
        assert all(isinstance(skill, str) for skill in skills), "Skills must be strings"
        self.skills = skills


class RoleBasics(LabelBlockParse):
    """Relevant basics for a resume."""

    def __init__(
        self,
        company: str,
        start_date: str | datetime,
        end_date: str | datetime | None,
        reason_for_change: str | None,
        title: str,
    ):
        """Initialize the object."""

        assert isinstance(company, str), "Company name must be a string"
        assert isinstance(title, str), "Job title must be a string"
        assert isinstance(
            start_date,
            (datetime | str),
        ), "Start date must be a datetime object"
        assert isinstance(end_date, (datetime, str, type(None)))
        assert isinstance(reason_for_change, (str, type(None)))

        self.company = company
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%m/%Y")  # noqa: DTZ007
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%m/%Y")  # noqa: DTZ007
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.reason_for_change = reason_for_change

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "company": "company",
            "start date": "start_date",
            "end date": "end_date",
            "reason for change": "reason_for_change",
            "title": "title",
        }


class Role(BasicBlockParse):
    """Details of a single work-related experience."""

    def __init__(
        self,
        basics: RoleBasics | None,
        description: RoleDescription | None,
        responsibilities: RoleResponsibilities | None,
        skills: RoleSkills | None,
    ):
        """Initialize the object."""
        assert isinstance(
            basics,
            (RoleBasics, type(None)),
        ), "Basics must be a RoleBasics object or None"
        assert isinstance(
            description,
            (RoleDescription, type(None)),
        ), "Description must be a RoleDescription object or None"
        assert isinstance(
            responsibilities,
            (RoleResponsibilities, type(None)),
        ), "Responsibilities must be a RoleResponsibilities object or None"
        assert isinstance(
            skills,
            (RoleSkills, type(None)),
        ), "Skills must be a RoleSkills object or None"

        self.basics = basics
        self.description = description
        self.responsibilities = responsibilities
        self.skills = skills

    @staticmethod
    def expected_blocks() -> dict[str, type]:
        """Return the expected blocks for this object."""

        return {
            "basics": "basics",
            "description": "description",
            "responsibilities": "responsibilities",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks."""
        return {
            "basics": RoleBasics,
            "description": RoleDescription,
            "responsibilities": RoleResponsibilities,
            "skills": RoleSkills,
        }


class Roles(MultiBlockParse):
    """Details of work history."""

    def __init__(
        self,
        roles: list[Role],
    ):
        """Initialize with a list of Role objects."""

        assert isinstance(roles, list), "Roles must be a list"
        assert all(
            isinstance(role, Role) for role in roles
        ), "Roles must be Role objects"

        log.info(f"Creating Roles object with {len(roles)} roles.")

        self.roles = roles

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
