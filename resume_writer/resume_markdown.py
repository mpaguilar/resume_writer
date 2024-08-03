import logging
from datetime import datetime

from models.roles import Roles
from resume_model import (
    Certification,
    Education,
    Personal,
    Resume,
)

log = logging.getLogger(__name__)


class MarkdowResumeParserError(Exception):
    """Exception raised for errors in the input."""


class MarkdownResumeParser:
    """Parse a markdown file into a Resume object."""

    def __init__(self, file_path: str):
        """Initialize the parser."""
        assert isinstance(file_path, str), "file_path must be a string"
        self.file_path = file_path

    def parse_job_basics_block(
        self,
        block_lines: list[str],
    ) -> tuple[str | None, str | None, datetime | None, datetime | None, str | None]:
        """Parse a block of job basics info.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings containing job basics information.

        Returns
        -------
        tuple[str | None, str | None, datetime | None, datetime | None, str | None]
            A tuple containing the parsed job title, company, start date, end date,
            and reason for change.

        Notes
        -----
        1. Initialize variables for title, company, start date, end date,
        and reason for change.
        2. Iterate through each line in the block of job basics info.
        3. If the line starts with "Title:", extract and store the title.
        4. If the line starts with "Company:", extract and store the company.
        5. If the line starts with "Start Date:", extract and store the start date.
        6. If the line starts with "End Date:", extract and store the end date.
        7. If the line starts with "Reason for Change:", extract and store the
        reason for change.
        8. Return the parsed job title, company, start date, end date, and reason for
        change.

        """

        assert isinstance(block_lines, list), "block_lines should be a list"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be strings"

        _title = None
        _company = None
        _started = None
        _ended = None
        _reason = None

        for _block_line in block_lines:
            if _block_line.lower().startswith("title:"):
                _title = _block_line.split(":")[1].strip()

            if _block_line.lower().startswith("company:"):
                _company = _block_line.split(":")[1].strip()

            if _block_line.lower().startswith("start date:"):
                _started_txt = _block_line.split(":")[1].strip()
                _started = datetime.strptime(_started_txt, "%m/%Y")  # noqa: DTZ007

            if _block_line.lower().startswith("end date:"):
                _ended_txt = _block_line.split(":")[1].strip()
                _ended = datetime.strptime(_ended_txt, "%m/%Y")  # noqa: DTZ007

            if _block_line.lower().startswith("reason for change:"):
                _reason = _block_line.split(":")[1].strip()

        assert isinstance(
            _title,
            (str, type(None)),
        ), "_title should be a string or None"
        assert isinstance(
            _company,
            (str, type(None)),
        ), "_company should be a string or None"
        assert isinstance(
            _started,
            (datetime, type(None)),
        ), "_started should be a datetime object or None"
        assert isinstance(
            _ended,
            (datetime, type(None)),
        ), "_ended should be a datetime object or None"
        assert isinstance(
            _reason,
            (str, type(None)),
        ), "_reason should be a string or None"

        return _title, _company, _started, _ended, _reason

    def parse(self) -> Resume:  # noqa: C901
        """Parse a markdown file into a Resume object.

        Allowed headers:
        - Personal
        - Work History
        - Education
        - Certifications
        - Awards

        """

        with open(self.file_path) as _file:
            _lines = _file.readlines()

        _ret = {}

        _personal: Personal | None = None
        _education: Education | None = None
        _work_history: Roles | None = None
        _certifications: list[Certification] | None = None

        _blocks = self.top_level_blocks(_lines)

        for _block_name, _block_lines in _blocks.items():
            _parsed_block = self.parse_block(
                block_name=_block_name,
                block_lines=_block_lines,
            )
            _ret[_block_name] = _parsed_block
            if _parsed_block is None:
                raise MarkdowResumeParserError(f"Unknown block: {_block_name}")
            if _block_name.lower() == "personal":
                _personal = _parsed_block
            elif _block_name.lower() == "education":
                _education = _parsed_block
            elif _block_name.lower() == "work history":
                _work_history = _parsed_block
            elif _block_name.lower() == "certifications":
                _certifications = _parsed_block
            else:
                log.warning(f"Unknown block: {_block_name}")

        _missing_blocks: list[str] = []
        if _personal is None:
            _missing_blocks.append("Personal")
            _personal = Personal(None, None, None)

        if _education is None:
            _missing_blocks.append("Education")
            _education = Education([])

        if _work_history is None:
            _missing_blocks.append("Work History")
            _work_history = Roles(roles=[])

        if _certifications is None:
            _missing_blocks.append("Certifications")
            _certifications = []

        return Resume(
            personal=_personal,
            education=_education,
            work_history=_work_history,
            certifications=_certifications,
        )
