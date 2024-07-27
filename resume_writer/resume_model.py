from datetime import datetime, timedelta


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


class WorkHistory:
    """Details of work history."""

    def __init__(
        self,
        roles: list[Role],
    ):
        """Initialize the object."""
        self.roles = roles


class Resume:
    """Resume details."""

    def __init__(
        self,
        personal: Personal,
        education: list[Education],
        work_history: WorkHistory,
        certifications: list[str],
    ):
        """Initialize the object."""

        assert isinstance(
            personal,
            Personal,
        ), "personal must be an instance of Personal"
        assert isinstance(education, list), "education must be a list"
        assert all(
            isinstance(edu, Education) for edu in education
        ), "education must be a list of Education instances"
        assert isinstance(
            work_history,
            WorkHistory,
        ), "work_history must be an instance of WorkHistory"
        assert isinstance(certifications, list), "certifications must be a list"
        assert all(
            isinstance(cert, str) for cert in certifications
        ), "certifications must be a list of strings"

        self.personal = personal
        self.education = education
        self.work_history = work_history
        self.certifications = certifications

    @property
    def years_of_experience(self) -> int:
        """Return the number of years of experience.

        1. Collect all the start and end dates of the roles.
        2. Sort the end dates in ascending order.
        3. for every start date, find the next end date that is greater than it.
        4. subtract the start date from the end date and add it to the total experience.
        5. return the total experience in years.
        """

        _total_experience = timedelta()
        _roles = sorted(self.role, key=lambda x: x.start_date)
        for _role in _roles:
            if _role.duration is not None:
                _end_date = datetime.now()  # noqa: DTZ005
                for _next_role in _roles:
                    if _next_role.start_date > _role.end_date:
                        _end_date = _next_role.start_date
                        break
                    _end_date = _next_role.end_date
                _duration = _end_date - _role.start_date
                _total_experience += _duration

        return round(_total_experience.days / 365, 1)

    def stats(self) -> dict[str, int]:
        """Return a dictionary of statistics about the resume."""

        _total_experience = timedelta()
        for role in self.work_history.role:
            if role.duration is not None:
                _total_experience += role.duration

        return {
            "education": len(self.education),
            "roles": len(self.work_history),
            "certifications": len(self.certifications),
            "total_experience": self.years_of_experience,
        }
