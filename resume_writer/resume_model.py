from datetime import datetime


class Role:
    """Details of a single work-related experience."""

    def __init__(  # noqa: PLR0913
        self,
        company: str,
        title: str,
        start_date: datetime,
        end_date: datetime | None,
        description: str | None,
        responsibilities: str,
        reason_for_change: str | None,
        skills: list[str],
    ):
        """Initialize the object."""
        assert isinstance(company, str), "Company name must be a string"
        assert isinstance(title, str), "Job title must be a string"
        assert isinstance(start_date, datetime), "Start date must be a datetime object"
        assert isinstance(end_date, (datetime, type(None)))
        assert isinstance(
            description,
            (str, type(None)),
        )
        assert isinstance(responsibilities, str), "Responsibilities must be a string"
        assert isinstance(reason_for_change, (str, type(None)))

        self.company = company
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.responsibilities = responsibilities
        self.description = description
        self.reason_for_change = reason_for_change
        self.skills = skills

        ## how should I handle the case where the person is currently working there?
        ## how should I handle new position in the same company?


class Education:
    """Details of educational background."""

    def __init__(
        self,
        school: str | None,
        degree: str | None,
        start_date: datetime | None,
        end_date: datetime | None,
    ):
        """Initialize the object."""
        assert isinstance(school, (str, type(None)))
        assert isinstance(degree, (str, type(None)))
        assert isinstance(start_date, (datetime, type(None)))
        assert isinstance(end_date, (datetime, type(None)))

        self.school = school
        self.degree = degree
        self.start_date = start_date
        self.end_date = end_date


class Certification:
    """Details of a certification."""

    def __init__(self, issuer: str | None, name: str | None, issued: datetime | None):
        """Initialize the object."""
        assert isinstance(name, (str, type(None)))
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(issued, (datetime, type(None)))

        self.name = name
        self.issued = issued
        self.issuer = issuer


class Personal:
    """Details of personal information."""

    def __init__(
        self,
        personal_info: "PersonalInfo | None",
        banner: str | None,
        note: str | None,
    ):
        """Initialize the object."""

        self.personal_info = personal_info
        self.banner = banner
        self.note = note


class PersonalInfo:
    """Details of personal information."""

    def __init__(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ):
        """Initialize the object."""

        self.name = name
        self.email = email
        self.phone = phone


class Resume:
    """Resume details."""

    def __init__(
        self,
        personal: Personal,
        education: list[Education],
        work_history: list[Role],
        certifications: list[str],
    ):
        """Initialize the object."""

        self.personal = personal
        self.education = education
        self.work_history = work_history
        self.certifications = certifications
