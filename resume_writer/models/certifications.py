import logging
from datetime import datetime

import dateparser

from resume_writer.models.parsers import (
    LabelBlockParse,
    MultiBlockParse,
    ParseContext,
)

log = logging.getLogger(__name__)


class Certification(LabelBlockParse):
    """Represents a professional certification.

    Base class:
        LabelBlockParse

    Attributes:
        name (str): The name of the certification.
        issuer (str | None): The organization that issued the certification.
        issued (datetime | None): The date the certification was issued.
        expires (datetime | None): The date the certification expires.
        certification_id (str | None): An identifier for the certification.
        parse_context (ParseContext): The context used during parsing, tracking line information.

    """

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        issuer: str | None,
        issued: datetime | str | None,
        expires: datetime | str | None,
        certification_id: str | None,
        parse_context: ParseContext,
    ):
        """Initialize a Certification object.

        Args:
            name: The name of the certification.
            issuer: The organization that issued the certification. Can be None.
            issued: The date the certification was issued. Can be a datetime object or a string.
            expires: The date the certification expires. Can be a datetime object or a string.
            certification_id: An identifier for the certification. Can be None.
            parse_context: The context used during parsing, tracking line information.

        Returns:
            None

        Notes:
            1. Validate that all inputs are of the correct type.
            2. If `issued` is a string, parse it into a datetime object using dateparser with PREFER_DAY_OF_MONTH set to "first".
            3. If `expires` is a string, parse it into a datetime object using dateparser with PREFER_DAY_OF_MONTH set to "first".
            4. Assign the parsed or original values to instance attributes.

        """
        assert isinstance(name, str)
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(issued, (datetime, str, type(None)))
        assert isinstance(expires, (datetime, str, type(None)))
        assert isinstance(certification_id, (str, type(None)))
        assert isinstance(parse_context, ParseContext)

        # If the issued date is a string, convert it to a datetime object
        if isinstance(issued, str):
            issued = dateparser.parse(
                issued,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            )

        if isinstance(expires, str):
            expires = dateparser.parse(
                expires,
                settings={
                    "PREFER_DAY_OF_MONTH": "first",
                },
            )

        self.issuer: str | None = issuer
        self.name: str = name
        self.issued: datetime | None = issued
        self.expires: datetime | None = expires
        self.certification_id: str | None = certification_id
        self.parse_context: ParseContext = parse_context

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object.

        Args:
            None

        Returns:
            A dictionary mapping field names (as strings) to their corresponding constructor argument names.

        Notes:
            1. The keys are field names as they appear in the input, and the values are the argument names used in the constructor.
            2. The field "certification id" maps to "certification_id" in the constructor.

        """
        return {
            "issuer": "issuer",
            "name": "name",
            "issued": "issued",
            "expires": "expires",
            "certification id": "certification_id",
        }


class Certifications(MultiBlockParse):
    """Represents a collection of professional certifications.

    Base class:
        MultiBlockParse

    Attributes:
        certifications (list[Certification]): A list of Certification objects.
        parse_context (ParseContext): The context used during parsing, tracking line information.

    """

    def __init__(
        self,
        certifications: list[Certification],
        parse_context: ParseContext,
    ):
        """Initialize a Certifications object.

        Args:
            certifications: A list of Certification objects.
            parse_context: The context used during parsing, tracking line information.

        Returns:
            None

        Notes:
            1. Assign the provided list of certifications to the instance attribute `certifications`.
            2. Assign the provided parse_context to the instance attribute `parse_context`.

        """
        self.certifications = certifications
        self.parse_context = parse_context

    def __iter__(self):
        """Iterate over the certifications.

        Args:
            None

        Returns:
            An iterator over the list of certification objects.

        Notes:
            1. Return an iterator over the `certifications` list.

        """
        return iter(self.certifications)

    def __len__(self):
        """Return the number of certifications.

        Args:
            None

        Returns:
            The integer count of certifications in the list.

        Notes:
            1. Return the length of the `certifications` list.

        """
        return len(self.certifications)

    @staticmethod
    def list_class() -> type:
        """Return the type that will be contained in the list.

        Args:
            None

        Returns:
            The Certification class.

        Notes:
            1. Return the Certification class, which is the type of objects in the list.

        """
        return Certification
