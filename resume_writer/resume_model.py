import logging
from datetime import datetime, timedelta
from typing import TypeVar

from models.parsers import BasicBlockParse, LabelBlockParse, MultiBlockParse
from models.roles import Roles

log = logging.getLogger(__name__)

T = TypeVar("T")

"""
The overall resume or any given block of text will contain only one of the following:
 - Only a mix of uniquely-named top level blocks
 - Only one or more blocks of the same name
 - Only label-value pairs
 - Only plain text
"""



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


class Certification(LabelBlockParse):
    """Details of a certification."""

    def __init__(
        self,
        issuer: str | None,
        name: str | None,
        issued: str | datetime | None,
    ):
        """Initialize the object."""
        assert isinstance(name, (str, type(None)))
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(issued, (str, datetime, type(None)))

        if isinstance(issued, str):
            issued = datetime.strptime(issued, "%m/%Y")  # noqa: DTZ007

        self.name = name
        self.issued = issued
        self.issuer = issuer

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "issuer": "issuer",
            "name": "name",
            "issued": "issued",
        }


class Certifications(MultiBlockParse):
    """Details of professional credentials."""

    def __init__(self, certifications: list[Certification]):
        """Initialize the object."""
        self.certifications = certifications

    def __iter__(self):
        """Iterate over the certifications."""
        return iter(self.certifications)

    @staticmethod
    def list_class() -> type:
        """Return the type that will be contained in the list."""
        return Certification


class Personal(BasicBlockParse):
    """Details of personal information.

    Text contains 3 sections:
    1. Info: Personal information
    2. Banner: Banner text
    3. Note: Note text

    """

    def __init__(
        self,
        personal_info: "PersonalInfo | None",
        banner: list[str] | None,
        note: list[str] | None,
    ):
        """Initialize the object."""

        self.personal_info = personal_info
        self.banner = banner
        self.note = note

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks."""

        return {
            "Info": "personal_info",
            "Banner": "banner",
            "Note": "note",
        }


class PersonalInfo(LabelBlockParse):
    """Details of personal information.

    Text contains lables and values. Labels without values should be omitted:
    1. Name: John Doe
    2. Email: name@example.com
    3. Phone: 123-456-7890
    4. Website: https://www.example.com
    5. Github: https://github.com/example
    6. LinkedIn: https://www.linkedin.com/in/example/
    7. Work Authorization: US Citizen/Green Card
    8. Require Sponsorship: Yes/No
    9. Twitter: https://twitter.com/example
    10. Location: Texas, USA

    """

    def __init__(  # noqa:PLR0913
        self,
        name: str | None,
        email: str | None,
        phone: str | None,
        website: str | None,
        github: str | None,
        linkedin: str | None,
        work_authorization: str | None,
        require_sponsorship: bool | None,
        twitter: str | None,
        location: str | None,
    ):
        """Initialize the object."""

        self.name = name
        self.email = email
        self.phone = phone

        self.website: str | None = website
        self.github: str | None = github
        self.linkedin: str | None = linkedin
        self.work_authorization: str | None = work_authorization
        self.require_sponsorship: bool | None = require_sponsorship
        self.twitter: str | None = twitter
        self.location: str | None = location

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected constructor fields."""

        # A label may contain spaces or other characters
        # these need to be translated into argument names
        _fields = {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "website": "website",
            "linkedin": "linkedin",
            "github": "github",
            "twitter": "twitter",
            "work authorization": "work_authorization",
            "require sponsorship": "require_sponsorship",
            "location": "location",
        }

        return _fields




class Resume:
    """Resume details."""

    def __init__(
        self,
        personal: Personal,
        education: Education,
        work_history: Roles,
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
            Roles,
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
