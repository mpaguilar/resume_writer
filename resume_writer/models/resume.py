import logging

from resume_writer.models.certifications import Certifications
from resume_writer.models.education import Education
from resume_writer.models.experience import Experience
from resume_writer.models.parsers import BasicBlockParse, ParseContext
from resume_writer.models.personal import Personal

log = logging.getLogger(__name__)


class Resume(BasicBlockParse):
    """Represents a resume.

    This class models a resume document, organizing personal information, education, work experience, and certifications.
    It uses a parsing framework to extract structured data from a text-based resume input.

    Attributes:
        personal (Personal | None): Personal information such as name, contact details, and summary.
        education (Education | None): Educational background, including degrees and institutions.
        experience (Experience | None): Work history, including job titles, companies, and responsibilities.
        certifications (Certifications | None): Professional certifications held by the individual.
        parse_context (ParseContext): Contextual information used during parsing of the resume.

    """

    def __init__(
        self,
        parse_context: ParseContext,
        personal: Personal | None,
        education: Education | None,
        experience: Experience | None,
        certifications: Certifications | None,
    ):
        """Initialize a Resume instance.

        Args:
            parse_context (ParseContext): The parsing context containing the input lines and line numbers.
            personal (Personal | None): Parsed personal information, or None if not present.
            education (Education | None): Parsed education details, or None if not present.
            experience (Experience | None): Parsed work experience, or None if not present.
            certifications (Certifications | None): Parsed certifications, or None if not present.

        Returns:
            None: This method initializes the instance and does not return a value.

        Notes:
            1. Validate that parse_context is an instance of ParseContext.
            2. Validate that personal is either an instance of Personal or None.
            3. Validate that education is either an instance of Education or None.
            4. Validate that experience is either an instance of Experience or None.
            5. Validate that certifications is either an instance of Certifications or None.
            6. Assign the provided arguments to instance attributes.
            7. No disk, network, or database access occurs during initialization.

        """
        assert isinstance(parse_context, ParseContext)
        assert isinstance(personal, (Personal, type(None)))
        assert isinstance(education, (Education, type(None)))
        assert isinstance(experience, (Experience, type(None)))
        assert isinstance(certifications, (Certifications, type(None)))

        self.personal = personal
        self.education = education
        self.experience = experience
        self.certifications = certifications
        self.parse_context = parse_context

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected block names and their corresponding constructor arguments.

        Args:
            None: This method takes no arguments.

        Returns:
            dict[str, str]: A dictionary mapping block names (e.g., "personal") to their constructor argument names (e.g., "personal").
            The keys are strings representing block types, and the values are identical strings matching the constructor parameter names.

        Notes:
            1. Return a dictionary with keys "personal", "education", "experience", and "certifications".
            2. Each key maps to the same string value (e.g., "personal" → "personal").
            3. This method is used by the parsing framework to determine how to process each block.
            4. No disk, network, or database access occurs.

        """
        return {
            "personal": "personal",
            "education": "education",
            "experience": "experience",
            "certifications": "certifications",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the class types for each expected block.

        Args:
            None: This method takes no arguments.

        Returns:
            dict[str, type]: A dictionary mapping block names (strings) to their corresponding class types.
            The keys are block names such as "personal", and the values are the corresponding class types (e.g., Personal).

        Notes:
            1. Return a dictionary with keys "personal", "education", "experience", "certifications".
            2. Each key maps to the corresponding class (Personal, Education, Experience, Certifications).
            3. This method is used by the parsing framework to instantiate each block during parsing.
            4. No disk, network, or database access occurs.

        """
        return {
            "personal": Personal,
            "education": Education,
            "experience": Experience,
            "certifications": Certifications,
        }
