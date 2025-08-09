import logging
from datetime import datetime

log = logging.getLogger(__name__)


class DateStats:
    """Provide date-range related statistics.

    Attributes:
        date_ranges (list[tuple[datetime, datetime]]): A list of date ranges
            represented as tuples of start and end datetimes.
    """

    def __init__(self):
        """Initialize the DateStats class.

        Initializes an empty list to store date ranges.
        """
        self.date_ranges = []

    def add_date_range(
        self,
        start_date: datetime,
        end_date: datetime | None = None,
    ) -> None:
        """Add a date range to the list of date ranges.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime | None): The end date of the range. If None,
                the current date is used.

        Returns:
            None

        Notes:
            1. Validate that start_date is not after end_date.
            2. If end_date is None, use the current date as end_date.
            3. Append the (start_date, end_date) tuple to the date_ranges list.
        """
        # Check if the start date is before the end date
        if end_date and start_date > end_date:
            raise ValueError("Start date must be before end date")

        _end_date = datetime.now() if end_date is None else end_date  # noqa: DTZ005

        self.date_ranges.append((start_date, _end_date))

    def merge_date_ranges(self) -> list[tuple[datetime, datetime]]:
        """Take a list of date ranges, and consolidate them.

        This function merges overlapping or adjacent date ranges into a single
        continuous range.

        Returns:
            list[tuple[datetime, datetime]]: A list of merged date ranges,
                each represented as a tuple of start and end datetimes.

        Notes:
            1. If no date ranges exist, return an empty list.
            2. Sort date ranges by start date.
            3. Initialize the first range as the current range.
            4. Iterate through the remaining ranges:
                a. If the current range overlaps with the next range (next start <= current end),
                   extend the current end date to the maximum of the two.
                b. Otherwise, add the current range to the merged list and start a new range.
            5. Add the final current range to the merged list.
            6. Return the merged ranges.
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
        """Return the total number of days across all merged date ranges.

        Returns:
            int: The total number of days of experience.

        Notes:
            1. Merge all date ranges using merge_date_ranges.
            2. Initialize a counter for total days.
            3. For each merged date range, add the number of days between start and end dates.
            4. Return the total.
        """
        _merged_ranges = self.merge_date_ranges()

        _total_days = 0

        for _start, _end in _merged_ranges:
            _total_days += (_end - _start).days

        assert _total_days >= 0, "_total_experience must be greater than 0"
        return _total_days

    @property
    def years_of_experience(self) -> float:
        """Return the number of years of experience.

        Returns:
            float: The number of years of experience, rounded to one decimal place.

        Notes:
            1. Compute the total days of experience.
            2. Divide by 365.25 to account for leap years.
            3. Round to one decimal place.
        """
        _yoe = self.days_of_experience / 365.25
        return round(_yoe, 1)

    @property
    def span_of_experience(self) -> float:
        """Return the span of experience from first to last date.

        Returns:
            float: The span of experience in years, rounded to one decimal place.

        Notes:
            1. Merge all date ranges using merge_date_ranges.
            2. Get the first start date and the last end date from the merged ranges.
            3. Calculate the difference between last end and first start.
            4. Divide by 365.25 to get years.
            5. Round to one decimal place.
        """
        _merged_ranges = self.merge_date_ranges()

        _first_date = _merged_ranges[0][0]
        _last_date = _merged_ranges[-1][1]

        _span = _last_date - _first_date
        _yoe = _span.days / 365.25
        return round(float(_yoe), 1)
