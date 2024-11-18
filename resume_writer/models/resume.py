import logging

from resume_writer.models.certifications import Certifications
from resume_writer.models.education import Education
from resume_writer.models.experience import Experience
from resume_writer.models.parsers import BasicBlockParse, ParseContext
from resume_writer.models.personal import Personal

log = logging.getLogger(__name__)


class Resume(BasicBlockParse):
    """Represents a resume."""

    def __init__(
        self,
        parse_context : ParseContext,
        personal: Personal | None,
        education: Education | None,
        experience: Experience | None,
        certifications: Certifications | None,
    ):
        """Initialize the object."""

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
        """Return the expected blocks for this object."""

        return {
            "personal": "personal",
            "education": "education",
            "experience": "experience",
            "certifications": "certifications",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        """Return the block classes for this object."""

        return {
            "personal": Personal,
            "education": Education,
            "experience": Experience,
            "certifications": Certifications,
        }
