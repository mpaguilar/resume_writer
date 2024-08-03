import logging

from models.parsers import BasicBlockParse, LabelBlockParse, TextBlockParse

log = logging.getLogger(__name__)


class ContactInfo(LabelBlockParse):
    """Details of personal contact information."""

    def __init__(
        self,
        name: str,
        email: str | None,
        phone: str | None,
        location: str | None,
    ):
        """Initialize the object."""

        assert isinstance(name, str), "Name must be a string"
        assert isinstance(email, (str, type(None))), "Email must be a string or None"
        assert isinstance(phone, (str, type(None))), "Phone must be a string or None"
        assert isinstance(
            location,
            (str, type(None)),
        ), "Location must be a string or None"

        self.name = name
        self.email = email
        self.phone = phone
        self.location = location

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected labels."""

        return {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "location": "location",
        }


class Websites(LabelBlockParse):
    """Details of personal websites."""

    def __init__(
        self,
        website: str | None,
        github: str | None,
        linkedin: str | None,
        twitter: str | None,
    ):
        """Initialize the object."""

        assert isinstance(
            website,
            (str, type(None)),
        ), "Website must be a string or None"
        assert isinstance(github, (str, type(None))), "Github must be a string or None"
        assert isinstance(
            linkedin,
            (str, type(None)),
        ), "Linkedin must be a string or None"
        assert isinstance(
            twitter,
            (str, type(None)),
        ), "Twitter must be a string or None"

        self.website = website
        self.github = github
        self.linkedin = linkedin
        self.twitter = twitter

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected labels."""

        return {
            "website": "website",
            "github": "github",
            "linkedin": "linkedin",
            "twitter": "twitter",
        }


class VisaStatus(LabelBlockParse):
    """Details of personal visa information."""

    def __init__(
        self,
        work_authorization: str | None,
        require_sponsorship: bool | str | None,
    ):
        """Initialize the object."""

        assert isinstance(
            work_authorization,
            (str, type(None)),
        ), "Work authorization must be a string or None"
        assert isinstance(
            require_sponsorship,
            (bool, str, type(None)),
        ), "Require sponsorship must be a boolean or None"

        self.work_authorization = work_authorization

        # Convert string to boolean
        if isinstance(require_sponsorship, str):
            if require_sponsorship.lower() == "yes":
                self.require_sponsorship: bool = True
            elif require_sponsorship.lower() == "no":
                self.require_sponsorship: bool = False
        elif require_sponsorship is not None:
            self.require_sponsorship: bool = require_sponsorship
        else:
            self.require_sponsorship = None

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected labels."""

        return {
            "work authorization": "work_authorization",
            "require sponsorship": "require_sponsorship",
        }


class Banner(TextBlockParse):
    """Details of personal banner."""

    def __init__(self, banner: str):
        """Initialize the object."""

        assert isinstance(banner, str), "Banner must be a string"
        # remove leading and ending blank lines
        _banner_lines = banner.split("\n")
        # remove leading blank lines
        while _banner_lines[0] == "\n":
            _banner_lines.pop(0)

        # remove trailing blank lines
        while _banner_lines[-1] == "\n":
            _banner_lines.pop()

        _banner = [line for line in _banner_lines if line.strip()]

        self.text = "\n".join(_banner)


class Note(TextBlockParse):
    """Details of personal note."""

    def __init__(self, note: str):
        """Initialize the object."""

        assert isinstance(note, str), "note must be a string"
        _note = note.split("\n")

        # remove leading blank lines
        while _note[0] == "\n":
            _note.pop(0)

        # remove trailing blank lines
        while _note[-1] == "\n":
            _note.pop()

        _note = [line for line in _note if line.strip()]

        self.text = "\n".join(_note)


class Personal(BasicBlockParse):
    """Details of personal information."""

    def __init__(
        self,
        contact_info: ContactInfo | None,
        websites: Websites | None,
        visa_status: VisaStatus | None,
        banner: Banner | None,
        note: Note | None,
    ):
        """Initialize the object."""

        assert isinstance(
            contact_info,
            (ContactInfo, type(None)),
        ), "Contact info must be a ContactInfo object or None"
        assert isinstance(
            websites,
            (Websites, type(None)),
        ), "Websites must be a Websites object or None"
        assert isinstance(
            visa_status,
            (VisaStatus, type(None)),
        ), "Visa status must be a VisaStatus object or None"
        assert isinstance(
            banner,
            (Banner, type(None)),
        ), "Banner must be a Banner object or None"
        assert isinstance(
            note,
            (Note, type(None)),
        ), "Note must be a Note object or None"

        self.contact_info = contact_info
        self.websites = websites
        self.visa_status = visa_status
        self.banner = banner
        self.note = note

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks."""

        return {
            "contact information": "contact_info",
            "websites": "websites",
            "visa status": "visa_status",
            "banner": "banner",
            "note": "note",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes for the blocks."""
        return {
            "contact information": ContactInfo,
            "websites": Websites,
            "visa status": VisaStatus,
            "banner": Banner,
            "note": Note,
        }
