import logging

from resume_writer.models.parsers import (
    BasicBlockParse,
    LabelBlockParse,
    ParseContext,
    TextBlockParse,
)

log = logging.getLogger(__name__)


class ContactInfo(LabelBlockParse):
    """Holds personal contact details such as name, email, phone, and location.

    Attributes:
        name (str): The full name of the person.
        email (str | None): The email address of the person, or None if not provided.
        phone (str | None): The phone number of the person, or None if not provided.
        location (str | None): The physical location (e.g., city and country) of the person, or None if not provided.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(
        self,
        parse_context: ParseContext,
        name: str,
        email: str | None,
        phone: str | None,
        location: str | None,
    ):
        """Initialize the contact information with provided details.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            name (str): The full name of the person.
            email (str | None): The email address of the person, or None if not provided.
            phone (str | None): The phone number of the person, or None if not provided.
            location (str | None): The physical location (e.g., city and country) of the person, or None if not provided.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that name is a string.
            3. Validate that email is either a string or None.
            4. Validate that phone is either a string or None.
            5. Validate that location is either a string or None.
            6. Assign the provided values to instance attributes.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
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
        self.parse_context = parse_context

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected labels for contact information fields.

        Args:
            None

        Returns:
            A dictionary mapping label names (e.g., "name", "email") to their corresponding attribute names in the ContactInfo class.

        Notes:
            1. The returned dictionary defines the expected field names in the input data for ContactInfo.
            2. The keys are the labels found in the input (e.g., "name", "email"), and the values are the corresponding attribute names in the class (e.g., "name").

        """
        return {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "location": "location",
        }


class Websites(LabelBlockParse):
    """Holds personal website and social media links.

    Attributes:
        website (str | None): The personal website URL, or None if not provided.
        github (str | None): The GitHub profile URL, or None if not provided.
        linkedin (str | None): The LinkedIn profile URL, or None if not provided.
        twitter (str | None): The Twitter profile URL, or None if not provided.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(
        self,
        parse_context: ParseContext,
        website: str | None,
        github: str | None,
        linkedin: str | None,
        twitter: str | None,
    ):
        """Initialize the websites information with provided links.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            website (str | None): The personal website URL, or None if not provided.
            github (str | None): The GitHub profile URL, or None if not provided.
            linkedin (str | None): The LinkedIn profile URL, or None if not provided.
            twitter (str | None): The Twitter profile URL, or None if not provided.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that website is either a string or None.
            3. Validate that github is either a string or None.
            4. Validate that linkedin is either a string or None.
            5. Validate that twitter is either a string or None.
            6. Assign the provided values to instance attributes.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

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

        self.parse_context = parse_context
        self.website = website
        self.github = github
        self.linkedin = linkedin
        self.twitter = twitter

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected labels for website and social media fields.

        Args:
            None

        Returns:
            A dictionary mapping label names (e.g., "website", "github") to their corresponding attribute names in the Websites class.

        Notes:
            1. The returned dictionary defines the expected field names in the input data for Websites.
            2. The keys are the labels found in the input (e.g., "website", "github"), and the values are the corresponding attribute names in the class (e.g., "website").

        """
        return {
            "website": "website",
            "github": "github",
            "linkedin": "linkedin",
            "twitter": "twitter",
        }


class VisaStatus(LabelBlockParse):
    """Holds information about work authorization and sponsorship requirements.

    Attributes:
        work_authorization (str | None): The current work authorization status (e.g., "US Citizen", "H-1B"), or None if not provided.
        require_sponsorship (bool | None): A boolean indicating if sponsorship is required, or None if not provided.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(
        self,
        parse_context: ParseContext,
        work_authorization: str | None,
        require_sponsorship: bool | str | None,
    ):
        """Initialize the visa status with provided authorization and sponsorship details.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            work_authorization (str | None): The current work authorization status (e.g., "US Citizen", "H-1B"), or None if not provided.
            require_sponsorship (bool | str | None): A boolean indicating if sponsorship is required, or a string ("yes"/"no") that will be converted to a boolean, or None if not provided.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that work_authorization is either a string or None.
            3. Validate that require_sponsorship is a boolean, string ("yes"/"no"), or None.
            4. Assign the provided work_authorization value to the instance attribute.
            5. If require_sponsorship is a string, convert "yes" to True and "no" to False.
            6. If require_sponsorship is not None and not a string, assign it directly.
            7. Otherwise, set require_sponsorship to None.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"

        assert isinstance(
            work_authorization,
            (str, type(None)),
        ), "Work authorization must be a string or None"
        assert isinstance(
            require_sponsorship,
            (bool, str, type(None)),
        ), "Require sponsorship must be a boolean or None"

        self.work_authorization = work_authorization
        self.parse_context = parse_context

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
        """Return the expected labels for visa and sponsorship fields.

        Args:
            None

        Returns:
            A dictionary mapping label names (e.g., "work authorization", "require sponsorship") to their corresponding attribute names in the VisaStatus class.

        Notes:
            1. The returned dictionary defines the expected field names in the input data for VisaStatus.
            2. The keys are the labels found in the input (e.g., "work authorization", "require sponsorship"), and the values are the corresponding attribute names in the class (e.g., "work_authorization").

        """
        return {
            "work authorization": "work_authorization",
            "require sponsorship": "require_sponsorship",
        }


class Banner(TextBlockParse):
    """Holds a personal banner message with cleaned text content.

    Attributes:
        text (str): The cleaned text content of the banner, with leading/trailing and internal blank lines removed.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(self, parse_context: ParseContext, text_string: str):
        """Initialize the banner with cleaned text content.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            text_string (str): The raw text content of the banner, potentially including leading/trailing or internal blank lines.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that text_string is a string.
            3. Split the input text_string into lines.
            4. Remove leading blank lines.
            5. Remove trailing blank lines.
            6. Filter out any lines that are blank after stripping whitespace.
            7. Join the remaining lines back into a single string and assign to self.text.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        assert isinstance(text_string, str), "Banner must be a string"

        # remove leading and ending blank lines
        _banner_lines = text_string.split("\n")
        # remove leading blank lines
        while _banner_lines[0] == "\n":
            _banner_lines.pop(0)

        # remove trailing blank lines
        while _banner_lines[-1] == "\n":
            _banner_lines.pop()

        _banner = [line for line in _banner_lines if line.strip()]

        self.text = "\n".join(_banner)


class Note(TextBlockParse):
    """Holds a personal note with cleaned text content.

    Attributes:
        text (str): The cleaned text content of the note, with leading/trailing and internal blank lines removed.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(self, parse_context: ParseContext, text_string: str):
        """Initialize the note with cleaned text content.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            text_string (str): The raw text content of the note, potentially including leading/trailing or internal blank lines.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that text_string is a string.
            3. Split the input text_string into lines.
            4. Remove leading blank lines.
            5. Remove trailing blank lines.
            6. Filter out any lines that are blank after stripping whitespace.
            7. Join the remaining lines back into a single string and assign to self.text.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        assert isinstance(text_string, str), "note must be a string"

        _note = text_string.split("\n")

        # remove leading blank lines
        while _note[0] == "\n":
            _note.pop(0)

        # remove trailing blank lines
        while _note[-1] == "\n":
            _note.pop()

        _note = [line for line in _note if line.strip()]

        self.text = "\n".join(_note)


class Personal(BasicBlockParse):
    """Holds all personal information including contact details, websites, visa status, banner, and note.

    Attributes:
        contact_info (ContactInfo | None): An instance of ContactInfo containing personal contact details, or None if not provided.
        websites (Websites | None): An instance of Websites containing personal website links, or None if not provided.
        visa_status (VisaStatus | None): An instance of VisaStatus containing visa and sponsorship information, or None if not provided.
        banner (Banner | None): An instance of Banner containing a personal banner message, or None if not provided.
        note (Note | None): An instance of Note containing a personal note, or None if not provided.
        parse_context (ParseContext): The context used during parsing, containing metadata about the input.

    """

    def __init__(  # noqa: PLR0913
        self,
        parse_context: ParseContext,
        contact_info: ContactInfo | None,
        websites: Websites | None,
        visa_status: VisaStatus | None,
        banner: Banner | None,
        note: Note | None,
    ):
        """Initialize the personal information block with provided components.

        Args:
            parse_context (ParseContext): The context used during parsing, containing metadata about the input.
            contact_info (ContactInfo | None): An instance of ContactInfo containing personal contact details, or None if not provided.
            websites (Websites | None): An instance of Websites containing personal website links, or None if not provided.
            visa_status (VisaStatus | None): An instance of VisaStatus containing visa and sponsorship information, or None if not provided.
            banner (Banner | None): An instance of Banner containing a personal banner message, or None if not provided.
            note (Note | None): An instance of Note containing a personal note, or None if not provided.

        Returns:
            None

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that contact_info is either a ContactInfo instance or None.
            3. Validate that websites is either a Websites instance or None.
            4. Validate that visa_status is either a VisaStatus instance or None.
            5. Validate that banner is either a Banner instance or None.
            6. Validate that note is either a Note instance or None.
            7. Assign the provided values to instance attributes.

        """
        assert isinstance(
            parse_context,
            ParseContext,
        ), "Parse context must be a ParseContext object"
        self.parse_context = parse_context

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

        self.parse_context = parse_context
        self.contact_info = contact_info
        self.websites = websites
        self.visa_status = visa_status
        self.banner = banner
        self.note = note

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected block names for parsing personal information.

        Args:
            None

        Returns:
            A dictionary mapping block names (e.g., "contact information") to their corresponding attribute names in the Personal class.

        Notes:
            1. The returned dictionary defines the expected block names in the input data for Personal.
            2. The keys are the block names found in the input (e.g., "contact information"), and the values are the corresponding attribute names in the class (e.g., "contact_info").

        """
        return {
            "contact information": "contact_info",
            "websites": "websites",
            "visa status": "visa_status",
            "banner": "banner",
            "note": "note",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the classes used to parse each block of personal information.

        Args:
            None

        Returns:
            A dictionary mapping block names (e.g., "contact information") to the corresponding class types for parsing.

        Notes:
            1. The returned dictionary defines which classes should be used to parse each block.
            2. The keys are the block names found in the input (e.g., "contact information"), and the values are the corresponding class types (e.g., ContactInfo).

        """
        return {
            "contact information": ContactInfo,
            "websites": Websites,
            "visa status": VisaStatus,
            "banner": Banner,
            "note": Note,
        }
