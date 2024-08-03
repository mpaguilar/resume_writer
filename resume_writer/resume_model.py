import logging
from datetime import datetime, timedelta
from typing import TypeVar

from models.certifications import Certification
from models.education import Education
from models.personal import Personal
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
