import logging
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


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


class Degree:
    """Details of a specific degree."""

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


class Education:
    """Details of educational background."""

    def __init__(self, degrees: list[Degree]):
        """Initialize the object."""
        self.degrees = degrees


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
        education: Education,
        work_history: WorkHistory,
        certifications: list[Certification],
    ):
        """Initialize the object."""

        assert isinstance(
            personal,
            Personal,
        ), "personal must be an instance of Personal"
        assert isinstance(education, Education), "education must be an Education object"
        assert isinstance(
            work_history,
            WorkHistory,
        ), "work_history must be an instance of WorkHistory"
        assert isinstance(certifications, list), "certifications must be a list"
        assert all(
            isinstance(cert, Certification) for cert in certifications
        ), "certifications must be a list of Certification objects"

        self.personal = personal
        self.education = education
        self.work_history = work_history
        self.certifications = certifications

    @property
    def years_of_experience(self) -> int:
        """Return the number of years of experience."""

        _total_duration = timedelta()

        _date_ranges = []
        for _role in self.work_history.roles:
            _end_date = datetime.now() if _role.end_date is None else _role.end_date  # noqa: DTZ005

            _date_ranges.append((_role.start_date, _end_date))

        _merged_ranges = self._merge_date_ranges(_date_ranges)

        _total_days = 0

        for _start, _end in _merged_ranges:
            _total_days += (_end - _start).days

        _total_duration = round(_total_days / 365, 1)

        assert _total_duration >= 0, "_total_experience must be greater than 0"
        return _total_duration

    def _merge_date_ranges(
        self,
        date_ranges: list[tuple[datetime, datetime]],
    ) -> list[tuple[datetime, datetime]]:
        _sorted_ranges = sorted(date_ranges, key=lambda x: x[0])
        _merged_ranges = []

        _current_start_date, _current_end_date = _sorted_ranges[0]

        for _start, _end in _sorted_ranges[1:]:
            if _start <= _current_end_date:  # overlapping
                _current_end_date = max(_current_end_date, _end)
            else:
                _merged_ranges.append((_current_start_date, _current_end_date))
                _current_start_date, _current_end_date = _start, _end
        _merged_ranges.append((_current_start_date, _current_end_date))
        return _merged_ranges

    @property
    def career_experience(self) -> float:
        """Return the total number of years of experience."""

        _start_dates = [x.start_date for x in self.work_history.roles]
        _end_dates = [x.end_date for x in self.work_history.roles]

        _first_start_date = min(_start_dates)
        _last_end_date = max(_end_dates)

        # Calculate the total number of years of experience
        _total_career_experience = round(
            (_last_end_date - _first_start_date).days / 365,
            1,
        )
        return _total_career_experience

    def stats(self) -> dict[str, int]:
        """Return a dictionary of statistics about the resume."""

        return {
            "education": len(self.education.degrees),
            "roles": len(self.work_history.roles),
            "certifications": len(self.certifications),
            "total_experience": self.years_of_experience,
            "career_experience": self.career_experience,
        }
