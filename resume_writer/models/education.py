import logging
from datetime import datetime

from models.parsers import BasicBlockParse, LabelBlockParse, MultiBlockParse

log = logging.getLogger(__name__)


class Degree(LabelBlockParse):
    """Details of a specific degree."""

    def __init__(
        self,
        school: str,
        degree: str | None,
        start_date: str | datetime | None,
        end_date: str | datetime | None,
    ):
        """Initialize the object."""
        assert isinstance(school, str)
        assert isinstance(degree, (str, type(None)))
        assert isinstance(start_date, (str, datetime, type(None)))
        assert isinstance(end_date, (str, datetime, type(None)))

        if school:
            log.debug(f"Creating degree object for {school}.")

        self.school = school
        self.degree = degree
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%m/%Y")  # noqa: DTZ007
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%m/%Y")  # noqa: DTZ007
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "school": "school",
            "degree": "degree",
            "start date": "start_date",
            "end date": "end_date",
        }


class Degrees(MultiBlockParse):
    """Details of educational background."""

    def __init__(self, degrees: list[Degree]):
        """Initialize the object."""

        assert isinstance(degrees, list)
        assert all(isinstance(degree, Degree) for degree in degrees)

        if degrees:
            log.info(f"Creating degrees object with {len(degrees)} degrees.")
        else:
            log.info("Creating degrees object with no degrees.")

        self.degrees = degrees

    def __iter__(self):
        """Iterate over the degrees."""
        return iter(self.degrees)

    def __len__(self):
        """Return the number of degrees."""
        return len(self.degrees)

    def __getitem__(self, index: int):
        """Return the degree at the given index."""
        return self.degrees[index]

    @staticmethod
    def list_class() -> type:
        """Return the list class for this object."""
        return Degree


class Education(BasicBlockParse):
    """Details of educational background."""

    def __init__(self, degrees: Degrees | None):
        """Initialize the object."""
        assert isinstance(degrees, (Degrees, type(None)))
        if degrees:
            log.info(f"Creating education object with {len(degrees)} degrees.")
        else:
            log.info("Creating education object with no degrees.")
        self.degrees = degrees

    @staticmethod
    def expected_blocks() -> dict[str, type]:
        """Return the expected blocks for the Education object."""

        return {"degrees": "degrees"}

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the block classes for the Education object."""
        return {"degrees": Degrees}
