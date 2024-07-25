import logging
from datetime import datetime

from resume_model import Certification, Education, Personal, PersonalInfo, Role

log = logging.getLogger(__name__)


class MarkdownResumeParser:
    """Parse a markdown file into a Resume object."""

    def __init__(self, file_path: str):
        """Initialize the parser."""
        self.file_path = file_path

    def parse_personal_block(
        self,
        block_lines: list[str],
    ) -> Personal:
        """Parse a block of personal information.

        Allowed headers:
        - Info
        - Banner
        - Note

        """
        _personal_info = PersonalInfo()
        _banner = None
        _note = None

        _blocks = self.top_level_blocks(block_lines)
        for _block_name, _block_lines in _blocks.items():
            # Parse the block lines into a PersonalInfo object.
            if _block_name.lower() == "info":
                _name = None
                _email = None
                _phone = None
                for _block_line in _block_lines:
                    if _block_line.lower().startswith("name:"):
                        _name = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("email:"):
                        _email = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("phone:"):
                        _phone = _block_line.split(":")[1].strip()

                _personal_info = PersonalInfo(
                    name=_name,
                    email=_email,
                    phone=_phone,
                )

            if _block_name.lower() == "banner":
                _banner = "".join(_block_lines)

            if _block_name.lower() == "note":
                _note = "".join(_block_lines)

        _personal = Personal(
            personal_info=_personal_info,
            banner=_banner,
            note=_note,
        )

        return _personal

    def parse_certification(self, block_lines: list[str]) -> Certification:
        """Parse a block of certification info."""

        _certification = None

        _name: str | None = None
        _issuer: str | None = None
        _issued: datetime | None = None

        for _line in block_lines:
            _line = _line.strip()

            if _line.lower().startswith("name:"):
                _name = _line.split(":")[1].strip()
            if _line.lower().startswith("issuer:"):
                _issuer = _line.split(":")[1].strip()
            if _line.lower().startswith("issued:"):
                _issued_txt = _line.split(":")[1].strip()
                _issued = datetime.strptime(_issued_txt, "%m/%Y")  # noqa: DTZ007

        _certification = Certification(
            name=_name,
            issuer=_issuer,
            issued=_issued,
        )

        return _certification

    def parse_certifications_block(self, block_lines: list[str]) -> list[str]:
        """Parse a block of multiple certifications.

        Allowed headers:
        - Certification

        """

        _certifications: list[Certification] = []

        _certification_blocks = self.top_level_multi_blocks(block_lines)

        for _block in _certification_blocks:
            _certification = self.parse_certification(_block)
            _certifications.append(_certification)

        return _certifications

    def parse_education_block(
        self,
        block_lines: list[str],
    ) -> list[Education]:
        """Parse a block of education info.

        Allowed headers:
        - Degree

        """

        _education: list[Education] = []

        _blocks = self.top_level_blocks(block_lines)
        for _block_name, _block_lines in _blocks.items():
            if _block_name.lower() == "degree":
                for _block_line in _block_lines:
                    # Parse the block lines into a Education object.
                    if _block_line.lower().startswith("degree:"):
                        _degree = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("school:"):
                        _school = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("started:"):
                        _started_txt = _block_line.split(":")[1].strip()
                        _started = datetime.strptime(_started_txt, "%m/%Y")  # noqa: DTZ007
                    if _block_line.lower().startswith("ended:"):
                        _ended_txt = _block_line.split(":")[1].strip()
                        _ended = datetime.strptime(_ended_txt, "%m/%Y")  # noqa: DTZ007

                _degree = Education(
                    degree=_degree,
                    school=_school,
                    start_date=_started,
                    end_date=_ended,
                )
                _education.append(_degree)

        return _education

    def parse_job_basics_block(
        self,
        block_lines: list[str],
    ) -> tuple[str | None, str | None, datetime | None, datetime | None, str | None]:
        """Parse a block of job basics info."""

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

        return _title, _company, _started, _ended, _reason

    def parse_skills_block(self, block_lines: list[str]) -> list[str]:
        """Parse a block of skills info."""

        # Parse the block lines into a list of skills.
        _skills = []
        for _block_line in block_lines:
            if _block_line.lower().startswith("* ") or _block_line.lower().startswith(
                "- ",
            ):
                _skills.append(_block_line.strip()[2:])  # noqa: PERF401 # too long for list comp

        return _skills

    def parse_role_block(self, block_lines: list[str]) -> Role:
        """Parse a block of job info.

        Allowed headers:
        - Basics
        - Description
        - Responsibilities
        - Skills

        """

        _description = None
        _responsibilities = None
        _skills: list = []

        _blocks = self.top_level_blocks(block_lines)
        log.debug(f"workhistory _blocks: {_blocks.keys()}")

        for _block_name, _block_lines in _blocks.items():
            if _block_name.lower() == "basics":
                _title, _company, _started, _ended, _reason = (
                    self.parse_job_basics_block(_block_lines)
                )

            if _block_name.lower() == "description" and len(_block_lines) > 0:
                _description = "\n".join(_block_lines)

            if _block_name.lower() == "responsibilities" and len(_block_lines) > 0:
                _responsibilities = "".join(_block_lines)

            if _block_name.lower() == "skills":
                _skills = self.parse_skills_block(_block_lines)

        _job = Role(
            title=_title,
            company=_company,
            start_date=_started,
            end_date=_ended,
            reason_for_change=_reason,
            description=_description,
            responsibilities=_responsibilities,
            skills=_skills,
        )

        return _job

    def parse_work_history_block(
        self,
        block_lines: list[str],
    ) -> list[Role]:
        """Parse a block of work history info.

        Allowed headers:
        - Role

        """
        _work_history: list[Role] = []

        _role_blocks = self.top_level_multi_blocks(block_lines)
        for _role_block in _role_blocks:
            _role = self.parse_role_block(_role_block)
            _work_history.append(_role)

        return _work_history

    def top_level_multi_blocks(self, lines: list[str]) -> list[list[str]]:
        """Handle multiple blocks which have the same name."""
        _blocks = []
        _current_block = []
        _section_header = None

        for _line in lines:
            _line = _line.strip()

            # skip empty lines
            if not _line:
                continue

            if _line.startswith("# "):
                _section_header = _line[1:].strip()
                log.info(f"Found section header: {_section_header}")
                if len(_current_block) > 0:
                    _blocks.append(list(_current_block))
                _current_block.clear()
                continue

            if _section_header is not None:
                if _line.startswith("#"):
                    # this is a subheader, we want the line, but not the extra level
                    _line = _line[1:]
                _current_block.append(_line)

        # Get the last block
        if len(_current_block) > 0:
            _blocks.append(list(_current_block))

        return _blocks

    def top_level_blocks(self, lines: list[str]) -> dict[str, list[str]]:
        """Get the top-level blocks of text from the list of strings.

        Parameters
        ----------
        lines : list[str]
            A list of strings representing the lines of text to be processed.

        Returns
        -------
        dict[str, list[str]]
            A dictionary where the keys are the top-level section headers and the values
            are lists of strings representing the lines of text under each section.

        Notes
        -----
        The function breaks the lines into markdown sections by header. It identifies
        top-level headers by checking if a line starts with '# '. Empty lines are
        skipped. Lines that don't start with a '#' are considered lines of text and
        are added to  the current section. If a line starts with a '#' but not
        '# ', it's considered a subheader and the hash is removed before adding
        it to the current section.

        """

        _blocks: dict = {}

        # break the lines into markdown sections by header
        for _line in lines:
            _line = _line.strip()

            # skip empty lines
            if not _line:
                continue

            # if the line starts with a '# ', it's a top-level header
            if _line.startswith("# "):
                _section_header = _line[1:].strip()
                log.info(f"Found section header: {_section_header}")
                _blocks[_section_header] = []
                continue

            # if the line doesn't start with a #, it's a line of text
            if _line and not _line.startswith("# "):
                if _line.startswith("#"):
                    # this is a subheader, add it without the hash
                    _line = _line[1:]
                _blocks[_section_header].append(_line)

        return _blocks

    def parse(self) -> dict[str, list[str]]:
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

        # break the lines into markdown sections by header

        # get the primary blocks
        # allowed values: Personal, Work History, Education, Certifications, Awards

        _blocks = self.top_level_blocks(_lines)

        for _block_name, _block_lines in _blocks.items():
            if _block_name.lower() == "personal":
                _personal = self.parse_personal_block(_block_lines)

            if _block_name.lower() == "education":
                _education = self.parse_education_block(_block_lines)

            if _block_name.lower() == "work history":
                _work_history = self.parse_work_history_block(_block_lines)

            if _block_name.lower() == "certifications":
                _certifications = self.parse_certifications_block(_block_lines)

        return _blocks
