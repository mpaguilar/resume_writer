import logging
from datetime import datetime

import dateparser

from resume_writer.models.parsers import (
    BasicBlockParse,
    LabelBlockParse,
    MultiBlockParse,
    ParseContext,
    ParseError,
)

log = logging.getLogger(__name__)


class Degree(LabelBlockParse):
    """Details of a specific degree."""

    def __init__(  # noqa: PLR0913
        self,
        parse_context: ParseContext,
        school: str,
        degree: str | None,
        start_date: str | datetime | None,
        end_date: str | datetime | None,
        major: str | None = None,
        gpa: str | None = None,
    ):
        """Initialize the object."""
        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext object."
        assert isinstance(school, str)
        assert isinstance(degree, (str, type(None)))
        assert isinstance(start_date, (str, datetime, type(None)))
        assert isinstance(end_date, (str, datetime, type(None)))
        assert isinstance(major, (str, type(None)))
        assert isinstance(gpa, (str, type(None)))

        if school:
            log.debug(f"Creating degree object for {school}.")

        if end_date and not start_date:
            raise ParseError(
                message="Education section: End date provided without start date.",
                parse_context=parse_context,
            )

        self.school = school
        self.degree = degree
        if isinstance(start_date, str):
            start_date = dateparser.parse(
                start_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            )
        if isinstance(end_date, str):
            end_date = dateparser.parse(
                end_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            )

        if start_date and end_date and start_date > end_date:
            raise ParseError(
                "Start date is after end date.",
                parse_context=parse_context,
            )

        self.start_date = start_date
        self.end_date = end_date
        self.major = major
        self.gpa = gpa
        self.parse_context = parse_context

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "school": "school",
            "degree": "degree",
            "start date": "start_date",
            "end date": "end_date",
            "major": "major",
            "gpa": "gpa",
        }


class Degrees(MultiBlockParse):
    """Details of educational background."""

    def __init__(self, degrees: list[Degree], parse_context : ParseContext):
        """Initialize the object."""

        assert isinstance(degrees, list)
        assert all(isinstance(degree, Degree) for degree in degrees)
        assert isinstance(parse_context, ParseContext)

        if degrees:
            log.info(f"Creating degrees object with {len(degrees)} degrees.")
        else:
            log.info("Creating degrees object with no degrees.")

        self.degrees = degrees
        self.parse_context = parse_context

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

    def __init__(self, degrees: Degrees | None, parse_context: ParseContext):
        """Initialize the object."""
        assert isinstance(degrees, (Degrees, type(None)))
        assert isinstance(parse_context, ParseContext)

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
