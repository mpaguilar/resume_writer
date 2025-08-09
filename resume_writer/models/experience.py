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
    """Represents a brief description of a professional role.

    Attributes:
        summary (str): The text content of the role summary.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object.

        Args:
            text_string (str): The text content of the role summary.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that text_string is a string.
            2. Validate that parse_context is a ParseContext object.
            3. Store the text_string as the summary and parse_context as the context.

        """
        assert isinstance(text_string, str), "Summary must be a string"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        # TODO: rename this to `text`
        self.summary = text_string
        self.parse_context = parse_context


class RoleResponsibilities(TextBlockParse):
    """Represents detailed descriptions of role responsibilities.

    Attributes:
        text (str): The text content of the responsibilities.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object.

        Args:
            text_string (str): The text content of the responsibilities.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that parse_context is a ParseContext object.
            2. Validate that text_string is a string.
            3. Raise a ParseError if text_string is not a string.
            4. Store the text_string as the text and parse_context as the context.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        if not isinstance(text_string, str):
            raise ParseError("Responsibilities must be a string", parse_context)
        self.text = text_string
        self.parse_context = parse_context


class RoleSkills(ListBlockParse):
    """Represents skills used in a professional role.

    Attributes:
        skills (List[str]): A list of non-empty, stripped skill strings.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, skills: list[str], parse_context: ParseContext) -> None:
        """Initialize the object.

        Args:
            skills (List[str]): A list of skill strings.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that parse_context is a ParseContext object.
            2. Validate that skills is a list.
            3. Validate that all items in skills are strings.
            4. Strip whitespace from each skill and filter out empty strings.
            5. Store the cleaned list of skills and parse_context.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        assert isinstance(skills, list), "Skills must be a list"
        assert all(isinstance(skill, str) for skill in skills), "Skills must be strings"
        self.skills = [skill.strip() for skill in skills if skill.strip() != ""]
        self.parse_context = parse_context

    def __iter__(self):
        """Iterate over the skills.

        Returns:
            Iterator over the skills list.

        """
        return iter(self.skills)

    def __len__(self):
        """Return the number of skills.

        Returns:
            int: The number of skills.

        """
        return len(self.skills)

    def __getitem__(self, index: int):
        """Return the skill at the given index.

        Args:
            index (int): The index of the skill to return.

        Returns:
            str: The skill at the specified index.

        """
        return self.skills


class RoleBasics(LabelBlockParse):
    """Represents basic information about a professional role.

    Attributes:
        company (str): The name of the company.
        start_date (datetime): The start date of the role.
        end_date (datetime | None): The end date of the role or None if still ongoing.
        title (str): The job title.
        reason_for_change (str | None): The reason for leaving the role or None.
        location (str | None): The job location or None.
        job_category (str | None): The category of the job or None.
        employment_type (str | None): The employment type or None.
        agency_name (str | None): The name of the agency or None.
        parse_context (ParseContext): The context object used for parsing.
    """

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
        """Initialize the object.

        Args:
            parse_context (ParseContext): The context object used for parsing.
            company (str): The name of the company.
            start_date (str | datetime): The start date of the role as a string or datetime object.
            end_date (str | datetime | None): The end date of the role as a string, datetime object, or None.
            reason_for_change (str | None): The reason for leaving the role as a string or None.
            title (str): The job title.
            location (str | None, optional): The job location as a string or None.
            job_category (str | None, optional): The category of the job as a string or None.
            employment_type (str | None, optional): The employment type as a string or None.
            agency_name (str | None, optional): The name of the agency as a string or None.

        Returns:
            None

        Notes:
            1. Validate that parse_context is a ParseContext object.
            2. Validate that company and title are strings.
            3. Validate that start_date is either a string or datetime.
            4. Validate that end_date is a string, datetime, or None.
            5. Validate that all other fields are appropriate types.
            6. Parse start_date and end_date using dateparser with UTC timezone.
            7. Store all fields as instance attributes.

        """
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
        """Return the expected fields for this object.

        Returns:
            A dictionary mapping label names to constructor argument names.

        """
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
    """Represents a complete professional role with all associated details.

    Attributes:
        basics (RoleBasics | None): The RoleBasics object containing role metadata.
        summary (RoleSummary | None): The RoleSummary object describing the role.
        responsibilities (RoleResponsibilities | None): The RoleResponsibilities object listing duties.
        skills (RoleSkills | None): The RoleSkills object listing skills used.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(
        self,
        parse_context: ParseContext,
        basics: RoleBasics | None,
        summary: RoleSummary | None,
        responsibilities: RoleResponsibilities | None,
        skills: RoleSkills | None,
    ):
        """Initialize the object.

        Args:
            parse_context (ParseContext): The context object used for parsing.
            basics (RoleBasics | None): The RoleBasics object containing role metadata.
            summary (RoleSummary | None): The RoleSummary object describing the role.
            responsibilities (RoleResponsibilities | None): The RoleResponsibilities object listing duties.
            skills (RoleSkills | None): The RoleSkills object listing skills used.

        Returns:
            None

        Notes:
            1. Validate that parse_context is a ParseContext object.
            2. Validate that basics is either a RoleBasics object or None.
            3. Validate that summary is either a RoleSummary object or None.
            4. Validate that responsibilities is either a RoleResponsibilities object or None.
            5. Validate that skills is either a RoleSkills object or None.
            6. Store the provided components as instance attributes.

        """
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
        """Return the expected blocks for this object.

        Returns:
            A dictionary mapping block names to constructor argument names.

        """
        return {
            "basics": "basics",
            "summary": "summary",
            "responsibilities": "responsibilities",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks.

        Returns:
            A dictionary mapping block names to their corresponding classes.

        """
        return {
            "basics": RoleBasics,
            "summary": RoleSummary,
            "responsibilities": RoleResponsibilities,
            "skills": RoleSkills,
        }


class Roles(MultiBlockParse):
    """Represents a collection of professional roles.

    Attributes:
        roles (List[Role]): A list of Role objects.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, roles: list[Role], parse_context: ParseContext):
        """Initialize the object.

        Args:
            roles (List[Role]): A list of Role objects.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that roles is a list.
            2. Validate that all items in roles are Role objects.
            3. Validate that parse_context is a ParseContext object.
            4. Store the roles list and parse_context.

        """
        assert isinstance(roles, list), "Roles must be a list"
        assert all(isinstance(role, Role) for role in roles), (
            "Roles must be a list of Role objects"
        )
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.roles = roles

    def __iter__(self):
        """Iterate over the roles.

        Returns:
            Iterator over the roles list.

        """
        return iter(self.roles)

    def __len__(self):
        """Return the number of roles.

        Returns:
            int: The number of roles.

        """
        return len(self.roles)

    def __getitem__(self, index: int):
        """Return the role at the given index.

        Args:
            index (int): The index of the role to return.

        Returns:
            Role: The role at the specified index.

        """
        return self.roles[index]

    @staticmethod
    def list_class() -> type:
        """Return the class for the list.

        Returns:
            The Role class.

        """
        return Role


class ProjectSkills(ListBlockParse):
    """Represents skills used in a project.

    Attributes:
        skills (List[str]): A list of non-empty, stripped skill strings.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, skills: list[str], parse_context: ParseContext):
        """Initialize the object.

        Args:
            skills (List[str]): A list of skill strings.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that skills is a list.
            2. Validate that all items in skills are strings.
            3. Validate that parse_context is a ParseContext object.
            4. Strip whitespace from each skill and filter out empty strings.
            5. Store the cleaned list of skills.

        """
        assert isinstance(skills, list), "Skills must be a list"
        assert all(isinstance(skill, str) for skill in skills), (
            "Skills must be a list of strings"
        )
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        self.skills = [s.strip() for s in skills]

    def __iter__(self):
        """Iterate over the skills.

        Returns:
            Iterator over the skills list.

        """
        return iter(self.skills)

    def __len__(self):
        """Return the number of skills.

        Returns:
            int: The number of skills.

        """
        return len(self.skills)

    def __getitem__(self, index: int):
        """Return the skill at the given index.

        Args:
            index (int): The index of the skill to return.

        Returns:
            str: The skill at the specified index.

        """
        return self.skills[index]


class ProjectOverview(LabelBlockParse):
    """Represents basic details of a project.

    Attributes:
        title (str): The title of the project.
        url (str | None): The URL for the project or None.
        url_description (str | None): A description of the URL or None.
        start_date (datetime | None): The start date as a datetime object or None.
        end_date (datetime | None): The end date as a datetime object or None.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(  # noqa: PLR0913
        self,
        title: str,
        parse_context: ParseContext,
        url: str | None = None,
        url_description: str | None = None,
        start_date: str | datetime | None = None,
        end_date: str | datetime | None = None,
    ):
        """Initialize ProjectOverview object.

        Args:
            title (str): The title of the project.
            parse_context (ParseContext): The context object used for parsing.
            url (str | None, optional): The URL for the project as a string or None.
            url_description (str | None, optional): A description of the URL as a string or None.
            start_date (str | datetime | None, optional): The start date as a string, datetime, or None.
            end_date (str | datetime | None, optional): The end date as a string, datetime, or None.

        Returns:
            None

        Notes:
            1. Validate that title is a string.
            2. Validate that url and url_description are strings or None.
            3. Validate that start_date and end_date are strings, datetimes, or None.
            4. Validate that parse_context is a ParseContext object.
            5. Parse start_date and end_date using dateparser with UTC timezone.
            6. Store all fields as instance attributes.

        """
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
        """Return the expected fields for this object.

        Returns:
            A dictionary mapping label names to constructor argument names.

        """
        return {
            "title": "title",
            "url": "url",
            "url description": "url_description",
            "start date": "start_date",
            "end date": "end_date",
        }


class ProjectDescription(TextBlockParse):
    """Represents a brief description of a project.

    Attributes:
        text (str): The text content of the project description.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, text_string: str, parse_context: ParseContext):
        """Initialize the object.

        Args:
            text_string (str): The text content of the project description.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that text_string is a string.
            2. Validate that parse_context is a ParseContext object.
            3. Store the text_string as the text.

        """
        assert isinstance(text_string, str), "Text must be a string"
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.text = text_string


class Project(BasicBlockParse):
    """Represents a complete project with all associated details.

    Attributes:
        overview (ProjectOverview): The ProjectOverview object containing project metadata.
        description (ProjectDescription): The ProjectDescription object describing the project.
        skills (ProjectSkills | None): The ProjectSkills object listing skills used.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(
        self,
        overview: ProjectOverview,
        description: ProjectDescription,
        skills: ProjectSkills | None,
        parse_context: ParseContext,
    ):
        """Initialize the object.

        Args:
            overview (ProjectOverview): The ProjectOverview object containing project metadata.
            description (ProjectDescription): The ProjectDescription object describing the project.
            skills (ProjectSkills | None): The ProjectSkills object listing skills used.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that overview is a ProjectOverview object.
            2. Validate that description is a ProjectDescription object.
            3. Validate that skills is a ProjectSkills object or None.
            4. Validate that parse_context is a ParseContext object.
            5. Store all components as instance attributes.

        """
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
        """Return the expected blocks for this object.

        Returns:
            A dictionary mapping block names to constructor argument names.

        """
        return {
            "overview": "overview",
            "description": "description",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks.

        Returns:
            A dictionary mapping block names to their corresponding classes.

        """
        return {
            "overview": ProjectOverview,
            "description": ProjectDescription,
            "skills": ProjectSkills,
        }


class Projects(MultiBlockParse):
    """Represents a collection of projects.

    Attributes:
        projects (List[Project]): A list of Project objects.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(self, projects: list[Project], parse_context: ParseContext):
        """Initialize the object.

        Args:
            projects (List[Project]): A list of Project objects.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that projects is a list.
            2. Validate that all items in projects are Project objects.
            3. Validate that parse_context is a ParseContext object.
            4. Store the projects list.

        """
        assert isinstance(projects, list), "Projects must be a list"
        assert all(isinstance(project, Project) for project in projects), (
            "Projects must be a list of Project objects"
        )

        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.projects = projects

    def __iter__(self):
        """Iterate over the projects.

        Returns:
            Iterator over the projects list.

        """
        return iter(self.projects)

    def __len__(self):
        """Return the number of projects.

        Returns:
            int: The number of projects.

        """
        return len(self.projects)

    def __getitem__(self, index: int):
        """Return the project at the given index.

        Args:
            index (int): The index of the project to return.

        Returns:
            Project: The project at the specified index.

        """
        return self.projects[index]

    @staticmethod
    def list_class() -> type:
        """Return the class of the list.

        Returns:
            The Project class.

        """
        return Project


class Experience(BasicBlockParse):
    """Represents a collection of professional experience including roles and projects.

    Attributes:
        roles (Roles | None): A Roles object containing work experience.
        projects (Projects | None): A Projects object containing project details.
        parse_context (ParseContext): The context object used for parsing.
    """

    def __init__(
        self,
        roles: Roles | None,
        projects: Projects | None,
        parse_context: ParseContext,
    ):
        """Initialize with a list of Role objects.

        Args:
            roles (Roles | None): A Roles object containing work experience.
            projects (Projects | None): A Projects object containing project details.
            parse_context (ParseContext): The context object used for parsing.

        Returns:
            None

        Notes:
            1. Validate that roles is a Roles object or None.
            2. Validate that projects is a Projects object or None.
            3. Validate that parse_context is a ParseContext object.
            4. Log the creation of an Experience object.
            5. Store the roles and projects as instance attributes.

        """
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
        """Return the expected blocks for this object.

        Returns:
            A dictionary mapping block names to constructor argument names.

        """
        return {
            "roles": "roles",
            "projects": "projects",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks.

        Returns:
            A dictionary mapping block names to their corresponding classes.

        """
        return {
            "roles": Roles,
            "projects": Projects,
        }
