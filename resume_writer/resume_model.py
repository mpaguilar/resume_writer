from datetime import datetime


class WorkExperience:
    """Details of work-related experience."""

    def __init__(  # noqa: PLR0913
        self,
        company: str,
        title: str,
        start_date: datetime,
        end_date: datetime,
        responsibilities: str,
        reason_for_change: str,
    ):
        """Initialize the object."""
        assert isinstance(company, str), "Company name must be a string"
        assert isinstance(title, str), "Job title must be a string"
        assert isinstance(start_date, datetime), "Start date must be a datetime object"
        assert isinstance(end_date, datetime), "End date must be a datetime object"
        assert isinstance(responsibilities, str), "Responsibilities must be a string"

        self.company = company
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.responsibilities = responsibilities
        self.reason_for_change = reason_for_change

        assert isinstance(
            reason_for_change,
            str,
        ), "Reason for leaving must be a string"

        ## how should I handle the case where the person is currently working there?
        ## how should I handle new position in the same company?


class Education:
    """Details of educational background."""

    def __init__(
        self,
        school: str,
        degree: str,
        start_date: datetime,
        end_date: datetime,
    ):
        """Initialize the object."""
        assert isinstance(school, str), "School name must be a string"
        assert isinstance(degree, str), "Degree must be a string"
        assert isinstance(start_date, datetime), "Start date must be a datetime object"
        assert isinstance(end_date, datetime), "End date must be a datetime object"

        self.school = school
        self.degree = degree
        self.start_date = start_date
        self.end_date = end_date


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
        personal_info: PersonalInfo,
        education: list[Education],
        experience: list[WorkExperience],
        certifications: list[str],
        description: str,
    ):
        """Initialize the object."""

        self.personal = personal_info
        self.education = education
        self.experience = experience
        self.certifications = certifications
        self.description = description
