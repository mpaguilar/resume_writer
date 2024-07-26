import logging
from datetime import datetime

from resume_model import Certification, Education, Personal, PersonalInfo, Resume, Role

log = logging.getLogger(__name__)


class MarkdownResumeParser:
    """Parse a markdown file into a Resume object."""

    def __init__(self, file_path: str):
        """Initialize the parser."""
        assert isinstance(file_path, str), "file_path must be a string"
        self.file_path = file_path

    def parse_personal_block(
        self,
        block_lines: list[str],
    ) -> Personal:
        """Parse a block of personal information from a list of strings.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings representing the personal information block.

        Returns
        -------
        Personal
            A Personal object containing the parsed personal information.

        Notes
        -----
        1. Initialize an empty PersonalInfo object and set banner and note to None.
        2. Split the block_lines into top-level blocks based on headers.
        3. For each block, parse the block lines into the appropriate attribute.
        4. Create a Personal object with the parsed personal information.
        5. Return the Personal object.

        Allowed headers:
        - Info
        - Banner
        - Note

        """

        assert isinstance(block_lines, list)
        assert all(isinstance(line, str) for line in block_lines)

        _personal_info = PersonalInfo()
        _banner = None
        _note = None

        _blocks = self.top_level_blocks(block_lines)
        for _block_name, _block_lines in _blocks.items():
            assert isinstance(_block_name, str)
            assert isinstance(_block_lines, list)
            assert all(isinstance(line, str) for line in _block_lines)

            # Parse the block lines into a PersonalInfo object.
            if _block_name.lower() == "info":
                _name = None
                _email = None
                _phone = None
                for _block_line in _block_lines:
                    assert isinstance(_block_line, str)
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

        assert isinstance(_personal, Personal)
        return _personal

    def parse_certification(self, block_lines: list[str]) -> Certification:
        """Parse a block of certification information.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings containing the certification information.

        Returns
        -------
        Certification
            A Certification object containing the parsed information.

        Raises
        ------
        AssertionError
            If the input is not a list of strings, or if the parsing fails.

        Notes
        -----
        1. Assert that the input is a list of strings.
        2. Initialize a Certification object with None values.
        3. Iterate through each line in the input list.
        4. If the line starts with "name:", extract the name and assign it to the
           Certification object.
        5. If the line starts with "issuer:", extract the issuer and assign it to the
           Certification object.
        6. If the line starts with "issued:", extract the issued date, convert it to a
           datetime object, and assign it to the Certification object.
        7. Assert that the Certification object is of type Certification.
        8. Return the Certification object.

        """

        assert isinstance(
            block_lines,
            list,
        ), f"Expected list, got {type(block_lines).__name__}"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be str"

        _certification = None

        _name: str | None = None
        _issuer: str | None = None
        _issued: datetime | None = None

        for _line in block_lines:
            _line = _line.strip()

            if _line.lower().startswith("name:"):
                _name = _line.split(":")[1].strip()
                assert isinstance(
                    _name,
                    str,
                ), f"Expected str, got {type(_name).__name__}"
            if _line.lower().startswith("issuer:"):
                _issuer = _line.split(":")[1].strip()
                assert isinstance(
                    _issuer,
                    str,
                ), f"Expected str, got {type(_issuer).__name__}"
            if _line.lower().startswith("issued:"):
                _issued_txt = _line.split(":")[1].strip()
                _issued = datetime.strptime(_issued_txt, "%m/%Y")  # noqa: DTZ007
                assert isinstance(
                    _issued,
                    datetime,
                ), f"Expected datetime, got {type(_issued).__name__}"

        _certification = Certification(
            name=_name,
            issuer=_issuer,
            issued=_issued,
        )
        assert isinstance(
            _certification,
            Certification,
        ), f"Expected Certification, got {type(_certification).__name__}"
        return _certification

    def parse_certifications_block(self, block_lines: list[str]) -> list[str]:
        """Parse a block of multiple certifications.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings representing the block of certifications.

        Returns
        -------
        list[str]
            A list of Certification objects parsed from the input block.

        Notes
        -----
        1. Assert that block_lines is a list of strings.
        2. Initialize an empty list to store the parsed Certification objects.
        3. Split the input block_lines into individual certification blocks.
        4. For each certification block, parse it into a Certification object.
        5. Append the parsed Certification object to the list.
        6. Assert that the final list contains only Certification objects.
        7. Return the list of Certification objects.


        Allowed headers:
        - Certification

        """
        assert isinstance(block_lines, list), "block_lines should be a list of strings"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be strings"

        _certifications: list[Certification] = []

        _certification_blocks = self.top_level_multi_blocks(block_lines)

        for _block in _certification_blocks:
            assert isinstance(_block, list), "_block should be a list"
            assert all(
                isinstance(line, str) for line in _block
            ), "All elements in _block should be strings"

            _certification = self.parse_certification(_block)
            assert isinstance(
                _certification,
                Certification,
            ), "_certification should be an instance of Certification"
            _certifications.append(_certification)

        assert isinstance(_certifications, list), "_certifications should be a list"
        assert all(
            isinstance(cert, Certification) for cert in _certifications
        ), "All elements in _certifications should be instances of Certification"

        return _certifications

    def parse_education_block(
        self,
        block_lines: list[str],
    ) -> list[Education]:
        """Parse a block of education info into a list of Education objects.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings representing the lines in the education block.

        Returns
        -------
        list[Education]
            A list of Education objects parsed from the input block lines.

        Notes
        -----
        1. Initialize an empty list to store Education objects.
        2. Split the input block lines into sub-blocks based on top-level headers.
        3. Iterate through the sub-blocks and parse the relevant information.
        4. If the sub-block header is 'Degree', extract the degree, school,
        start date, and end date information.
        5. Create an Education object with the extracted information.
        6. Append the Education object to the list of Education objects.
        7. Return the list of Education objects.

        Allowed headers:
        - Degree

        """
        assert isinstance(block_lines, list), "block_lines should be a list of strings"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be strings"

        _education: list[Education] = []

        _blocks = self.top_level_blocks(block_lines)
        for _block_name, _block_lines in _blocks.items():
            assert isinstance(_block_name, str), "Block names should be strings"
            assert isinstance(
                _block_lines,
                list,
            ), "Block lines should be a list of strings"
            assert all(
                isinstance(line, str) for line in _block_lines
            ), "All elements in block lines should be strings"

            if _block_name.lower() == "degree":
                for _block_line in _block_lines:
                    # Parse the block lines into a Education object.
                    if _block_line.lower().startswith("degree:"):
                        _degree = _block_line.split(":")[1].strip()
                        assert isinstance(_degree, str), "Degree should be a string"
                    if _block_line.lower().startswith("school:"):
                        _school = _block_line.split(":")[1].strip()
                        assert isinstance(_school, str), "School should be a string"
                    if _block_line.lower().startswith("started:"):
                        _started_txt = _block_line.split(":")[1].strip()
                        _started = datetime.strptime(_started_txt, "%m/%Y")  # noqa: DTZ007
                        assert isinstance(
                            _started,
                            datetime,
                        ), "Start date should be a datetime object"
                    if _block_line.lower().startswith("ended:"):
                        _ended_txt = _block_line.split(":")[1].strip()
                        _ended = datetime.strptime(_ended_txt, "%m/%Y")  # noqa: DTZ007
                        assert isinstance(
                            _ended,
                            datetime,
                        ), "End date should be a datetime object"

                _degree = Education(
                    degree=_degree,
                    school=_school,
                    start_date=_started,
                    end_date=_ended,
                )
                assert isinstance(
                    _degree,
                    Education,
                ), "Parsed data should be an Education object"
                _education.append(_degree)

        assert isinstance(_education, list), "Return value should be a list"
        assert all(
            isinstance(edu, Education) for edu in _education
        ), "All elements in the returned list should be Education objects"

        return _education

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

    def parse_skills_block(self, block_lines: list[str]) -> list[str]:
        """Parse a block of skills information.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings, where each string represents a line in a block of skills
            information.

        Returns
        -------
        list[str]
            A list of skills extracted from the input block lines.

        Notes
        -----
        1. Initialize an empty list to store the extracted skills.
        2. Iterate over each line in the input block lines.
        3. Check if the line starts with "* " or "- ".
        4. If the line starts with "* " or "- ", strip the leading "* " or "- "
            and append the result to the skills list.
        5. Return the list of extracted skills.

        """

        # Parse the block lines into a list of skills.
        assert isinstance(block_lines, list), "block_lines should be a list"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be strings"

        _skills = []
        for _block_line in block_lines:
            if _block_line.lower().startswith("* ") or _block_line.lower().startswith(
                "- ",
            ):
                _skills.append(_block_line.strip()[2:])  # noqa: PERF401 # too long for list comp

        assert isinstance(_skills, list), "The returned value should be a list"
        assert all(
            isinstance(skill, str) for skill in _skills
        ), "All elements in the returned list should be strings"

        return _skills

    def parse_role_block(self, block_lines: list[str]) -> Role:
        """Parse a block of job information.

        Allowed headers: Basics, Description, Responsibilities, Skills.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings representing the lines in the job block.

        Returns
        -------
        Role
            A Role object containing the parsed job information.

        Steps
        -----
        1. Initialize variables for description, responsibilities, and skills.
        2. Split the block lines into top-level blocks.
        3. Parse each top-level block based on its header.
        4. If the header is 'Basics', parse the job basics block.
        5. If the header is 'Description', join the block lines into a string.
        6. If the header is 'Responsibilities', join the block lines into a string.
        7. If the header is 'Skills', parse the skills block.
        8. Create a Role object with the parsed job information.
        9. Return the Role object.

        Allowed headers:
        - Basics
        - Description
        - Responsibilities
        - Skills

        """

        assert isinstance(block_lines, list), "block_lines should be a list of strings"

        _description = None
        _responsibilities = None
        _skills: list = []

        _blocks = self.top_level_blocks(block_lines)
        assert isinstance(_blocks, dict), "_blocks should be a dictionary"
        log.debug(f"role _blocks: {_blocks.keys()}")

        for _block_name, _block_lines in _blocks.items():
            assert isinstance(_block_name, str), "_block_name should be a string"
            assert isinstance(
                _block_lines,
                list,
            ), "_block_lines should be a list of strings"

            if _block_name.lower() == "basics":
                _title, _company, _started, _ended, _reason = (
                    self.parse_job_basics_block(_block_lines)
                )

                _msg = f"role _title: {_title}, _company: {_company}, "
                _msg += f"_started: {_started}, _ended: {_ended}, _reason: {_reason}"
                log.debug(_msg)

            assert isinstance(_title, str), "_title should be a string"
            assert isinstance(_company, str), "_company should be a string"
            assert isinstance(
                _started,
                datetime,
            ), "_started should be a datetime object"
            assert isinstance(_ended, datetime), "_ended should be a datetime object"
            assert isinstance(_reason, (str, type(None))), "_reason should be a string"

            if _block_name.lower() == "description" and len(_block_lines) > 0:
                _description = "\n".join(_block_lines)
                log.debug(f"role _description: {_description}")

            if _block_name.lower() == "responsibilities" and len(_block_lines) > 0:
                _responsibilities = "".join(_block_lines)
                log.debug(f"role _responsibilities: {_responsibilities}")

            if _block_name.lower() == "skills":
                _skills = self.parse_skills_block(_block_lines)
                log.debug(f"role _skills: {_skills}")

        _role = Role(
            title=_title,
            company=_company,
            start_date=_started,
            end_date=_ended,
            reason_for_change=_reason,
            description=_description,
            responsibilities=_responsibilities,
            skills=_skills,
        )

        log.debug(f"workhistory _role: {_role.title}")

        return _role

    def parse_work_history_block(
        self,
        block_lines: list[str],
    ) -> list[Role]:
        """Parse a block of work history information.

        This function takes a list of strings, each representing a line in a work
        history block, and returns a list of Role objects, each containing
        information about a single role.

        Parameters
        ----------
        block_lines : list[str]
            A list of strings, where each string is a line in a work history block.

        Returns
        -------
        list[Role]
            A list of Role objects, each containing information about a single
            role in the work history.

        Notes
        -----
        This function assumes that the input block_lines list contains valid work
        history information. It uses the `top_level_multi_blocks` function to split
        the block_lines into individual role blocks, and then calls the
        `parse_role_block` function to parse each role block into a Role object.

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
        """Handle multiple blocks which have the same name.

        Parameters
        ----------
        lines : list[str]
            A list of strings representing the lines of a document.

        Returns
        -------
        list[list[str]]
            A list of lists of strings, where each sublist represents a block of text.

        Notes
        -----
        1. Initialize an empty list to store the blocks and a current block.
        2. Iterate through each line in the input list.
        3. Skip empty lines.
        4. If a line starts with "# ", it's a section header. Append the current block
            to the list of blocks, clear the current block, and set the section header.
        5. If a line starts with "#" and a section header is set, it's a subheader.
            Remove the "#" and append the line to the current block.
        6. After iterating through all lines, append the current block to the
            list of blocks.
        7. Return the list of blocks.

        """

        assert isinstance(lines, list), "Expected 'lines' to be of type list[str]"
        assert all(
            isinstance(line, str) for line in lines
        ), "Expected all elements in 'lines' to be of type str"

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

        assert isinstance(
            _blocks,
            list,
        ), "Expected '_blocks' to be of type list[list[str]]"
        assert all(
            isinstance(block, list) for block in _blocks
        ), "Expected all elements in '_blocks' to be of type list[str]"
        assert all(
            all(isinstance(item, str) for item in block) for block in _blocks
        ), "Expected all elements in '_blocks' to be of type str"

        return _blocks

    def top_level_blocks(self, lines: list[str]) -> dict[str, list[str]]:
        """Extract top-level blocks of text from a list of strings.

        Parameters
        ----------
        lines : list[str]
            A list of strings representing the lines of text.

        Returns
        -------
        dict[str, list[str]]
            A dictionary where the keys are the top-level section headers and the
            values are lists of strings representing the lines of text in that
            section.

        Raises
        ------
        AssertionError
            If the input is not a list of strings or if the output is not a
            dictionary with string keys and list of strings values.

        Notes
        -----
        1. The function iterates over the list of strings.
        2. Empty lines are skipped.
        3. Top-level headers are identified by lines starting with '# '.
        4. Lines of text are added to the current section.
        5. Subheaders are added without the '#' character.
        6. The function asserts the types of the input and output to ensure
        consistency.

        """
        assert isinstance(lines, list), "lines should be a list of strings"
        assert all(
            isinstance(line, str) for line in lines
        ), "All elements in lines should be strings"

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
                assert isinstance(
                    _section_header,
                    str,
                ), "_section_header should be a string"
                log.debug(f"Found section header: {_section_header}")
                _blocks[_section_header] = []
                continue

            # if the line doesn't start with a #, it's a line of text
            if _line and not _line.startswith("# "):
                if _line.startswith("#"):
                    # this is a subheader, add it without the hash
                    _line = _line[1:]
                _blocks[_section_header].append(_line)

            assert isinstance(_blocks, dict), "_blocks should be a dictionary"
            assert all(
                isinstance(key, str) for key in _blocks
            ), "All keys in _blocks should be strings"
            assert all(
                isinstance(value, list) for value in _blocks.values()
            ), "All values in _blocks should be lists"
            assert all(
                all(isinstance(item, str) for item in value)
                for value in _blocks.values()
            ), "All elements in the lists of _blocks should be strings"

        return _blocks

    def parse(self) -> Resume:
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

        _blocks = self.top_level_blocks(_lines)

        for _block_name, _block_lines in _blocks.items():
            if _block_name.lower() == "personal":
                log.debug("Parsing personal block")
                _personal = self.parse_personal_block(_block_lines)

            if _block_name.lower() == "education":
                log.debug("Parsing education block")
                _education = self.parse_education_block(_block_lines)

            if _block_name.lower() == "work history":
                log.debug("Parsing work history block")
                _work_history = self.parse_work_history_block(_block_lines)

            if _block_name.lower() == "certifications":
                log.debug("Parsing certifications block")
                _certifications = self.parse_certifications_block(_block_lines)

        return Resume(
            personal=_personal,
            education=_education,
            work_history=_work_history,
            certifications=_certifications,
        )
