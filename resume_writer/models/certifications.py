import logging
from datetime import datetime

from models.parsers import (
    LabelBlockParse,
    MultiBlockParse,
)

log = logging.getLogger(__name__)


class Certification(LabelBlockParse):
    """Certifications block."""

    def __init__(
        self,
        issuer: str | None,
        name: str | None,
        issued: datetime | str | None,
        expires: datetime | str | None,
    ):
        """Initialize the object."""
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(name, (str, type(None)))
        assert isinstance(issued, (datetime, str, type(None)))
        assert isinstance(expires, (datetime, str, type(None)))

        # If the issued date is a string, convert it to a datetime object
        if isinstance(issued, str):
            issued = datetime.strptime(issued, "%m/%Y") # noqa: DTZ007

        if isinstance(expires, str):
            expires = datetime.strptime(expires, "%m/%Y") # noqa: DTZ007

        self.issuer = issuer
        self.name = name
        self.issued = issued
        self.expires = expires

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

    @staticmethod
    def list_class() -> type:
        """Return the type that will be contained in the list."""
        return Certification
