import logging

from models.certifications import Certifications
from models.education import Education
from models.experience import Experience
from models.parsers import BasicBlockParse
from models.personal import Personal

log = logging.getLogger(__name__)


class Resume(BasicBlockParse):
    """Represents a resume."""

    def __init__(
        self,
        personal: Personal | None,
        education: Education | None,
        experience: Experience | None,
        certifications: Certifications | None,
    ):
        """Initialize the object."""

        assert isinstance(personal, (Personal, type(None)))
        assert isinstance(education, (Education, type(None)))
        assert isinstance(experience, (Experience, type(None)))
        assert isinstance(certifications, (Certifications, type(None)))

        self.personal = personal
        self.education = education
        self.experience = experience
        self.certifications = certifications

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
