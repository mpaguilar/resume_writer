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
    """Represents details of a specific academic degree earned.

    Attributes:
        school (str): The name of the educational institution.
        degree (str | None): The type of degree (e.g., Bachelor, Master).
        start_date (datetime | None): The start date of the program.
        end_date (datetime | None): The end date of the program.
        major (str | None): The major field of study.
        gpa (str | None): The grade point average.
        parse_context (ParseContext): The context in which the parsing occurred.

    """

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
        """Initialize a Degree object with academic details.

        Args:
            parse_context: The context in which the parsing occurred, used for error reporting.
            school: The name of the educational institution.
            degree: The type of degree (e.g., Bachelor, Master).
            start_date: The start date of the program, as a string or datetime object.
            end_date: The end date of the program, as a string or datetime object.
            major: The major field of study.
            gpa: The grade point average, as a string.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that school is a non-empty string.
            3. Validate that degree, major, and gpa are either strings or None.
            4. Validate that start_date and end_date are either strings, datetime objects, or None.
            5. If end_date is provided but start_date is not, raise a ParseError.
            6. Parse start_date and end_date from strings into datetime objects using dateparser.
            7. If both start_date and end_date are provided, ensure start_date is not after end_date.
            8. Store the parsed values in the object's attributes.

        """
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
        """Return the expected fields for this object.

        Args:
            None

        Returns:
            A dictionary mapping field names to argument names.

        Notes:
            1. Return a dictionary with keys: "school", "degree", "start date", "end date", "major", "gpa".
            2. Each key maps to the corresponding argument name in the __init__ method.

        """
        return {
            "school": "school",
            "degree": "degree",
            "start date": "start_date",
            "end date": "end_date",
            "major": "major",
            "gpa": "gpa",
        }


class Degrees(MultiBlockParse):
    """Represents a collection of academic degrees earned.

    Attributes:
        degrees (list[Degree]): A list of Degree objects representing educational achievements.
        parse_context (ParseContext): The context in which the parsing occurred.

    """

    def __init__(self, degrees: list[Degree], parse_context: ParseContext):
        """Initialize a Degrees object with a list of degree records.

        Args:
            degrees: A list of Degree objects representing educational achievements.
            parse_context: The context in which the parsing occurred, used for error reporting.

        Returns:
            None

        Notes:
            1. Validate that degrees is a list.
            2. Validate that all items in degrees are instances of Degree.
            3. Validate that parse_context is an instance of ParseContext.
            4. Log the number of degrees created.
            5. Store the degrees list and parse_context in the object.

        """
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
        """Iterate over the degrees.

        Args:
            None

        Returns:
            An iterator over the degrees list.

        Notes:
            1. Return an iterator over the degrees list.

        """
        return iter(self.degrees)

    def __len__(self):
        """Return the number of degrees.

        Args:
            None

        Returns:
            The number of degrees in the list.

        Notes:
            1. Return the length of the degrees list.

        """
        return len(self.degrees)

    def __getitem__(self, index: int):
        """Return the degree at the given index.

        Args:
            index: The index of the degree to retrieve.

        Returns:
            The Degree object at the specified index.

        Notes:
            1. Return the degree at the given index from the degrees list.

        """
        return self.degrees[index]

    @staticmethod
    def list_class() -> type:
        """Return the list class for this object.

        Args:
            None

        Returns:
            The Degree class.

        Notes:
            1. Return the Degree class as the list class for this object.

        """
        return Degree


class Education(BasicBlockParse):
    """Represents the educational background section of a resume.

    Attributes:
        degrees (Degrees | None): A Degrees object containing educational achievements, or None if no degrees.
        parse_context (ParseContext): The context in which the parsing occurred.

    """

    def __init__(self, degrees: Degrees | None, parse_context: ParseContext):
        """Initialize an Education object with educational details.

        Args:
            degrees: A Degrees object containing educational achievements, or None if no degrees.
            parse_context: The context in which the parsing occurred, used for error reporting.

        Returns:
            None

        Notes:
            1. Validate that degrees is either a Degrees object or None.
            2. Validate that parse_context is an instance of ParseContext.
            3. Log the number of degrees in the object.
            4. Store the degrees and parse_context in the object.

        """
        assert isinstance(degrees, (Degrees, type(None)))
        assert isinstance(parse_context, ParseContext)

        if degrees:
            log.info(f"Creating education object with {len(degrees)} degrees.")
        else:
            log.info("Creating education object with no degrees.")
        self.degrees = degrees

    @staticmethod
    def expected_blocks() -> dict[str, type]:
        """Return the expected blocks for the Education object.

        Args:
            None

        Returns:
            A dictionary mapping block names to their corresponding classes.

        Notes:
            1. Return a dictionary with a single key "degrees" mapping to the Degrees class.

        """
        return {"degrees": "degrees"}

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the block classes for the Education object.

        Args:
            None

        Returns:
            A dictionary mapping block names to their corresponding classes.

        Notes:
            1. Return a dictionary with a single key "degrees" mapping to the Degrees class.

        """
        return {"degrees": Degrees}
