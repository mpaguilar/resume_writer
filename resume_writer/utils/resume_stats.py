import logging
from datetime import datetime

log = logging.getLogger(__name__)


class DateStats:
    """Provide date-range related statistics."""

    def __init__(self):
        """Initialize the DateStats class."""
        self.date_ranges = []

    def add_date_range(
        self,
        start_date: datetime,
        end_date: datetime | None = None,
    ) -> None:
        """Add a date range to the list of date ranges."""
        # Check if the start date is before the end date
        if end_date and start_date > end_date:
            raise ValueError("Start date must be before end date")

        _end_date = datetime.now() if end_date is None else end_date  # noqa: DTZ005

        self.date_ranges.append((start_date, _end_date))

    def merge_date_ranges(self) -> list[tuple[datetime, datetime]]:
        """Take a list of date ranges, and consolidate them.

        * Remove 0-length ranges.
        * Remove completely overlapped ranges.
        * Overlapping ranges should use the start of
            the first range and the end of the last range.
        """
        if len(self.date_ranges) == 0:
            log.warning("No date ranges to merge")
            return []

        _sorted_ranges = sorted(self.date_ranges, key=lambda x: x[0])
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
    def days_of_experience(self) -> int:
        """Return the number of years of experience."""
        _merged_ranges = self.merge_date_ranges()

        _total_days = 0

        for _start, _end in _merged_ranges:
            _total_days += (_end - _start).days

        assert _total_days >= 0, "_total_experience must be greater than 0"
        return _total_days

    @property
    def years_of_experience(self) -> float:
        """Return the number of years of experience."""
        _yoe = self.days_of_experience / 365.25
        return round(_yoe, 1)

    @property
    def span_of_experience(self) -> float:
        """Return the span of experience, from first time used to last."""
        _merged_ranges = self.merge_date_ranges()

        _first_date = _merged_ranges[0][0]
        _last_date = _merged_ranges[-1][1]

        _span = _last_date - _first_date
        _yoe = _span.days / 365.25
        return round(float(_yoe), 1)
