import logging
from datetime import datetime

from resume_model import Education, Personal, PersonalInfo, Role

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

        _blocks = self.get_top_level_blocks(block_lines)
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

    def parse_education_block(
        self,
        block_lines: list[str],
    ) -> list[Education]:
        """Parse a block of education info.

        Allowed headers:
        - Degree

        """

        _education: list[Education] = []

        _blocks = self.get_top_level_blocks(block_lines)
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

    def parse_job_block(self, block_lines: list[str]) -> Role:
        """Parse a block of job info.

        Allowed headers:
        - Basics
        - Description
        - Responsibilities
        - Skills

        """

        _blocks = self.get_top_level_blocks(block_lines)
        _description = None
        _responsibilities = None
        _skills: list = []

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

        _blocks = self.get_top_level_blocks(block_lines)
        _work_history = []

        # Parse the block lines into a list of roles.
        for _block_name, _block_lines in _blocks.items():
            if _block_name.lower() == "role":
                _role = self.parse_job_block(_block_lines)
                _work_history.append(_role)

        return _work_history

    def get_top_level_blocks(self, lines: list[str]) -> dict[str, list[str]]:
        """Get the top-level blocks of text from the list of strings.

        Read the lines.

        1. If the line starts with '# ', it's a top-level header.
        2. If the line doesn't start with a #, it's a line of text.
        3. If the line is empty, skip it.
        4. If the line starts with a #, start a new section.
        5. If the line doesn't start with a #, add it to the current section.
        5a. If the line starts with a #, it's a subheader.
            Remove the # and add it to the current section.
        6. Return a dictionary of sections.

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
        """Parse a markdown file into a Resume object."""

        with open(self.file_path) as _file:
            _lines = _file.readlines()

        # break the lines into markdown sections by header

        # get the primary blocks
        # allowed values: Personal, Work History, Education, Certifications, Awards

        _blocks = self.get_top_level_blocks(_lines)

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
