import logging
from datetime import datetime

import dateparser

from resume_writer.models.parsers import (
    LabelBlockParse,
    MultiBlockParse,
)

log = logging.getLogger(__name__)


class Certification(LabelBlockParse):
    """Certifications block."""

    def __init__(
        self,
        name: str,
        issuer: str | None,
        issued: datetime | str | None,
        expires: datetime | str | None,
    ):
        """Initialize the object."""
        assert isinstance(name, str)
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(issued, (datetime, str, type(None)))
        assert isinstance(expires, (datetime, str, type(None)))

        # If the issued date is a string, convert it to a datetime object
        if isinstance(issued, str):
            issued = dateparser.parse(issued, settings={
                "PREFER_DAY_OF_MONTH": "first",
            })

        if isinstance(expires, str):
            expires = dateparser.parse(expires, settings={
                "PREFER_DAY_OF_MONTH": "first",
            })

        self.issuer : str | None = issuer
        self.name : str = name
        self.issued : datetime | None = issued
        self.expires : datetime | None = expires

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "issuer": "issuer",
            "name": "name",
            "issued": "issued",
            "expires": "expires",
        }


class Certifications(MultiBlockParse):
    """Details of professional credentials."""

    def __init__(self, certifications: list[Certification]):
        """Initialize the object."""
        self.certifications = certifications

    def __iter__(self):
        """Iterate over the certifications."""
        return iter(self.certifications)

    def __len__(self):
        """Return the number of certifications."""
        return len(self.certifications)

    @staticmethod
    def list_class() -> type:
        """Return the type that will be contained in the list."""
        return Certification
