import logging
from datetime import datetime

import dateparser
import pytz

from resume_writer.models.parsers import (
    BasicBlockParse,
    LabelBlockParse,
    ListBlockParse,
    MultiBlockParse,
    ParseContext,
    ParseError,
    TextBlockParse,
)

log = logging.getLogger(__name__)


class RoleSummary(TextBlockParse):
    """Brief description of a role."""

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(text_string, str), "Summary must be a string"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        # TODO: rename this to `text`
        self.summary = text_string
        self.parse_context = parse_context


class RoleResponsibilities(TextBlockParse):
    """Detailed description of role responsibilities."""

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        if not isinstance(text_string, str):
            raise ParseError("Responsibilities must be a string", parse_context)
        self.text = text_string
        self.parse_context = parse_context


class RoleSkills(ListBlockParse):
    """Skills used in a role."""

    def __init__(self, skills: list[str], parse_context: ParseContext) -> None:
        """Initialize the object."""
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        assert isinstance(skills, list), "Skills must be a list"
        assert all(isinstance(skill, str) for skill in skills), "Skills must be strings"
        self.skills = [skill.strip() for skill in skills if skill.strip() != ""]
        self.parse_context = parse_context

    def __iter__(self):
        """Iterate over the skills."""
        return iter(self.skills)

    def __len__(self):
        """Return the number of skills."""
        return len(self.skills)

    def __getitem__(self, index: int):
        """Return the skill at the given index."""
        return self.skills


class RoleBasics(LabelBlockParse):
    """Relevant basics for a resume."""

    def __init__(  # noqa: PLR0913
        self,
        parse_context: ParseContext,
        company: str,
        start_date: str | datetime,
        end_date: str | datetime | None,
        reason_for_change: str | None,
        title: str,
        location: str | None = None,
        job_category: str | None = None,
        employment_type: str | None = None,
        agency_name: str | None = None,
    ):
        """Initialize the object."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        if not isinstance(company, str):
            raise ParseError(
                "Company name must be a string",
                parse_context=parse_context,
            )

        if not isinstance(title, str):
            raise ParseError("Job title must be a string", parse_context=parse_context)

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
            start_date = dateparser.parse(
                start_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                    "TIMEZONE": "UTC",
                },
            ).astimezone(pytz.utc)
        if isinstance(end_date, str):
            end_date = dateparser.parse(
                end_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                    "TIMEZONE": "UTC",
                },
            ).astimezone(pytz.utc)

        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.reason_for_change = reason_for_change
        self.location = location
        self.job_category = job_category
        self.employment_type = employment_type
        self.agency_name = agency_name
        self.parse_context = parse_context

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
        parse_context: ParseContext,
        basics: RoleBasics | None,
        summary: RoleSummary | None,
        responsibilities: RoleResponsibilities | None,
        skills: RoleSkills | None,
    ):
        """Initialize the object."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

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
        self.parse_context = parse_context

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


class Roles(MultiBlockParse):
    """Collection of work-related experiences."""

    def __init__(self, roles: list[Role], parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(roles, list), "Roles must be a list"
        assert all(
            isinstance(role, Role) for role in roles
        ), "Roles must be a list of Role objects"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
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
        """Return the class for the list."""
        return Role


class ProjectSkills(ListBlockParse):
    """Skills used in a project."""

    def __init__(self, skills: list[str], parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(skills, list), "Skills must be a list"
        assert all(
            isinstance(skill, str) for skill in skills
        ), "Skills must be a list of strings"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        self.skills = [s.strip() for s in skills]

    def __iter__(self):
        """Iterate over the skills."""
        return iter(self.skills)

    def __len__(self):
        """Return the number of skills."""
        return len(self.skills)

    def __getitem__(self, index: int):
        """Return the skill at the given index."""
        return self.skills[index]


class ProjectOverview(LabelBlockParse):
    """Basic details of a project."""

    def __init__(  # noqa: PLR0913
        self,
        title: str,
        parse_context: ParseContext,
        url: str | None = None,
        url_description: str | None = None,
        start_date: str | datetime | None = None,
        end_date: str | datetime | None = None,
    ):
        """Initialize ProjectOverview object."""

        assert isinstance(title, str), "Title must be a string"
        assert isinstance(url, (str, type(None))), "URL must be a string or None"
        assert isinstance(
            url_description,
            (str, type(None)),
        ), "URL description must be a string or None"
        assert isinstance(
            start_date,
            (str, datetime, type(None)),
        ), "Start date must be a string, datetime, or None"
        assert isinstance(
            end_date,
            (str, datetime, type(None)),
        ), "End date must be a string, datetime, or None"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        self.title = title
        self.url = url
        self.url_description = url_description
        if isinstance(start_date, str):
            start_date = dateparser.parse(
                start_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            ).astimezone(pytz.utc)
        if isinstance(end_date, str):
            end_date = dateparser.parse(
                end_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            ).astimezone(pytz.utc)
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "title": "title",
            "url": "url",
            "url description": "url_description",
            "start date": "start_date",
            "end date": "end_date",
        }


class ProjectDescription(TextBlockParse):
    """Brief description of a project."""

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(text_string, str), "Text must be a string"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.text = text_string


class Project(BasicBlockParse):
    """Details of a single project."""

    def __init__(
        self,
        overview: ProjectOverview,
        description: ProjectDescription,
        skills: ProjectSkills | None,
        parse_context: ParseContext,
    ):
        """Initialize the object."""
        assert isinstance(
            overview,
            ProjectOverview,
        ), "Overview must be a ProjectOverview object"
        assert isinstance(
            description,
            ProjectDescription,
        ), "Description must be a ProjectDescription object"
        assert isinstance(
            skills,
            (ProjectSkills, type(None)),
        ), "Skills must be a ProjectSkills object or None"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        self.overview = overview
        self.description = description
        self.skills = skills

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks for this object."""
        return {
            "overview": "overview",
            "description": "description",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks."""
        return {
            "overview": ProjectOverview,
            "description": ProjectDescription,
            "skills": ProjectSkills,
        }


class Projects(MultiBlockParse):
    """Collection of projects."""

    def __init__(self, projects: list[Project], parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(projects, list), "Projects must be a list"
        assert all(
            isinstance(project, Project) for project in projects
        ), "Projects must be a list of Project objects"

        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.projects = projects

    def __iter__(self):
        """Iterate over the projects."""
        return iter(self.projects)

    def __len__(self):
        """Return the number of projects."""
        return len(self.projects)

    def __getitem__(self, index: int):
        """Return the project at the given index."""
        return self.projects[index]

    @staticmethod
    def list_class() -> type:
        """Return the class of the list."""
        return Project


class Experience(BasicBlockParse):
    """Details of experience."""

    def __init__(
        self,
        roles: Roles | None,
        projects: Projects | None,
        parse_context: ParseContext,
    ):
        """Initialize with a list of Role objects."""

        assert isinstance(roles, (Roles, type(None))), "Roles must be a Roles object"
        assert isinstance(
            projects,
            (Projects, type(None)),
        ), "Projects must be a Projects object"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        log.info("Creating Experience object.")

        self.roles = roles
        self.projects = projects

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks for this object."""
        return {
            "roles": "roles",
            "projects": "projects",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks."""
        return {
            "roles": Roles,
            "projects": Projects,
        }
