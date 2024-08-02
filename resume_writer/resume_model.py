import logging
from datetime import datetime, timedelta
from typing import TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")

"""
The overall resume or any given block of text will contain only one of the following:
 - Only a mix of uniquely-named top level blocks
 - Only one or more blocks of the same name
 - Only label-value pairs
 - Only plain text
"""


class LabelBlockParse:
    """Mixin for parsing blocks for labels."""

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the block of lines into an object."""

        assert isinstance(block_lines, list)
        assert all(isinstance(line, str) for line in block_lines)

        _expected_fields = cls.expected_fields()
        _init_kwargs: dict[str, str | bool] = {}

        for _block_line in block_lines:
            _label = _block_line.split(":")[0].lower()  # for lookup
            _user_label = _block_line.split(":")[0]  # verbatim

            # lookup the label in the expected fields
            if _label in _expected_fields:
                # the argument name is the value of the label in the expected fields
                _init_arg = _expected_fields[_label]
                # remove the label from the line, leaving the value
                _value = _block_line.replace(f"{_user_label}:", "", 1).strip()
                # add the argument name and value to the init kwargs
                _init_kwargs[_init_arg] = _value
                # remove the label from the expected fields
                _expected_fields.pop(_label)

        # if there are any expected fields left, add them to the init kwargs with None
        _none_kwargs = {_field: None for _field in _expected_fields.values()}
        # update the init kwargs with the none kwargs
        _init_kwargs.update(_none_kwargs)

        return cls(**_init_kwargs)


class BasicBlockParse:
    """Mixin for blocks containing a mix of top level blocks."""

    @classmethod
    def parse_blocks(cls: T, block_lines: list[str]) -> dict[str, str]:
        """Parse the block of lines into a dictionary of blocks."""

        assert isinstance(block_lines, list), "block_lines should be a list"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "block_lines should be a list of strings"

        _blocks: dict = {}

        _section_header = None

        # iterate over the lines in the block
        for _block_line in block_lines:
            _block_line = _block_line.strip()

            # skip empty lines
            if not _block_line:
                continue

            # if the line starts with "# ", it's a section header
            if _block_line.startswith("# "):
                _section_header = _block_line[1:].strip()
                assert isinstance(
                    _section_header,
                    str,
                ), "_section_header should be a string"
                assert _section_header != "", "_section_header should not be empty"

                log.debug(f"Found section header: {_section_header}")
                _blocks[_section_header] = []
                continue

            if _section_header is None:
                # we haven't found a section header yet
                # this shouldn't happen, but we'll ignore it for now
                log.info(f"Found line without section header: {_block_line}")
                continue

            # if the line doesn't start with "#", it's a line of text
            if _block_line and not _block_line.startswith("# "):
                if _block_line.startswith("#"):
                    # this is a subheader, add it without the hash
                    _block_line = _block_line[1:]
                    log.debug(f"Found subheader: {_block_line}")
                _blocks[_section_header].append(_block_line)

        # check up on the values we've got so far
        assert isinstance(_blocks, dict), "_blocks should be a dictionary"
        assert all(
            isinstance(key, str) for key in _blocks
        ), "_blocks keys should be strings"
        assert all(
            isinstance(value, list) for value in _blocks.values()
        ), "_blocks values should be lists"
        assert all(
            isinstance(item, str) for value in _blocks.values() for item in value
        ), "_blocks values should be lists of strings"

        return _blocks

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the block of lines into an object."""

        _expected_blocks = cls.expected_blocks()
        _blocks: dict[str, str] = cls.parse_blocks(block_lines)

        _init_kwargs: dict[str, str] = {}
        for _block in _blocks:
            _lookup_block = _block.lower().strip()
            if _lookup_block in _expected_blocks:
                _init_arg = _expected_blocks[_lookup_block]
                _init_kwargs[_init_arg] = _block
                _expected_blocks.pop(_lookup_block)
            else:
                log.info(f"Unexpected block: {_block}")

        _none_kwargs = {_field: None for _field in _expected_blocks.values()}
        _init_kwargs.update(_none_kwargs)
        return cls(**_init_kwargs)


class MultiBlockParse:
    """Mixin for blocks containing multiple blocks with the same name."""

    @classmethod
    def parse_blocks(cls: T, block_lines: list[str]) -> list[list[str]]:
        """Handle multiple blocks which have the same name.

        Parameters
        ----------
        block_lines : list[str]
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
        4a. This is rather naive, it doesn't check the section name, it only assumes it
            is the one we're looking for.
        5. If a line starts with "#" and a section header is set, it's a subheader.
            Remove the "#" and append the line to the current block.
        6. After iterating through all lines, append the current block to the
            list of blocks.
        7. Return the list of blocks.

        """

        assert isinstance(block_lines, list), "Expected 'lines' to be of type list[str]"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "Expected all elements in 'lines' to be of type str"

        _blocks = []
        _current_block = []
        _section_header = None

        for _line in block_lines:
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


class Role:
    """Details of a single work-related experience."""

    def __init__(  # noqa: PLR0913
        self,
        company: str,
        title: str,
        start_date: datetime,
        end_date: datetime | None,
        description: str | None,
        responsibilities: str,
        reason_for_change: str | None,
        skills: list[str],
    ):
        """Initialize the object."""
        assert isinstance(company, str), "Company name must be a string"
        assert isinstance(title, str), "Job title must be a string"
        assert isinstance(start_date, datetime), "Start date must be a datetime object"
        assert isinstance(end_date, (datetime, type(None)))
        assert isinstance(
            description,
            (str, type(None)),
        )
        assert isinstance(responsibilities, str), "Responsibilities must be a string"
        assert isinstance(reason_for_change, (str, type(None)))

        self.company = company
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.responsibilities = responsibilities
        self.description = description
        self.reason_for_change = reason_for_change
        self.skills = skills


class Degree:
    """Details of a specific degree."""

    def __init__(
        self,
        school: str | None,
        degree: str | None,
        start_date: datetime | None,
        end_date: datetime | None,
    ):
        """Initialize the object."""
        assert isinstance(school, (str, type(None)))
        assert isinstance(degree, (str, type(None)))
        assert isinstance(start_date, (datetime, type(None)))
        assert isinstance(end_date, (datetime, type(None)))

        self.school = school
        self.degree = degree
        self.start_date = start_date
        self.end_date = end_date


class Education:
    """Details of educational background."""

    def __init__(self, degrees: list[Degree]):
        """Initialize the object."""
        self.degrees = degrees


class Certification(LabelBlockParse):
    """Details of a certification."""

    def __init__(
        self,
        issuer: str | None,
        name: str | None,
        issued: str | datetime | None,
    ):
        """Initialize the object."""
        assert isinstance(name, (str, type(None)))
        assert isinstance(issuer, (str, type(None)))
        assert isinstance(issued, (str, datetime, type(None)))

        if isinstance(issued, str):
            issued = datetime.strptime(issued, "%m/%Y")  # noqa: DTZ007

        self.name = name
        self.issued = issued
        self.issuer = issuer

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected fields for this object."""
        return {
            "issuer": "issuer",
            "name": "name",
            "issued": "issued",
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

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the blocks and return a list of objects."""

        _object_list: list[cls] = []
        _object_blocks = cls.parse_blocks(block_lines)
        _list_type = cls.list_class()

        for _block in _object_blocks:
            _object = _list_type.parse(_block)
            _object_list.append(_object)

        assert all(isinstance(obj, _list_type) for obj in _object_list)
        return _object_list


class Personal(BasicBlockParse):
    """Details of personal information.

    Text contains 3 sections:
    1. Info: Personal information
    2. Banner: Banner text
    3. Note: Note text

    """

    def __init__(
        self,
        personal_info: "PersonalInfo | None",
        banner: list[str] | None,
        note: list[str] | None,
    ):
        """Initialize the object."""

        self.personal_info = personal_info
        self.banner = banner
        self.note = note

    @staticmethod
    def expected_blocks() -> dict[str, str]:
        """Return the expected blocks."""

        return {
            "Info": "personal_info",
            "Banner": "banner",
            "Note": "note",
        }


class PersonalInfo(LabelBlockParse):
    """Details of personal information.

    Text contains lables and values. Labels without values should be omitted:
    1. Name: John Doe
    2. Email: name@example.com
    3. Phone: 123-456-7890
    4. Website: https://www.example.com
    5. Github: https://github.com/example
    6. LinkedIn: https://www.linkedin.com/in/example/
    7. Work Authorization: US Citizen/Green Card
    8. Require Sponsorship: Yes/No
    9. Twitter: https://twitter.com/example
    10. Location: Texas, USA

    """

    def __init__(  # noqa:PLR0913
        self,
        name: str | None,
        email: str | None,
        phone: str | None,
        website: str | None,
        github: str | None,
        linkedin: str | None,
        work_authorization: str | None,
        require_sponsorship: bool | None,
        twitter: str | None,
        location: str | None,
    ):
        """Initialize the object."""

        self.name = name
        self.email = email
        self.phone = phone

        self.website: str | None = website
        self.github: str | None = github
        self.linkedin: str | None = linkedin
        self.work_authorization: str | None = work_authorization
        self.require_sponsorship: bool | None = require_sponsorship
        self.twitter: str | None = twitter
        self.location: str | None = location

    @staticmethod
    def expected_fields() -> dict[str, str]:
        """Return the expected constructor fields."""

        # A label may contain spaces or other characters
        # these need to be translated into argument names
        _fields = {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "website": "website",
            "linkedin": "linkedin",
            "github": "github",
            "twitter": "twitter",
            "work authorization": "work_authorization",
            "require sponsorship": "require_sponsorship",
            "location": "location",
        }

        return _fields


class WorkHistory:
    """Details of work history."""

    def __init__(
        self,
        roles: list[Role],
    ):
        """Initialize the object."""
        self.roles = roles


class Resume:
    """Resume details."""

    def __init__(
        self,
        personal: Personal,
        education: Education,
        work_history: WorkHistory,
        certifications: list[Certification],
    ):
        """Initialize the object."""

        assert isinstance(
            personal,
            Personal,
        ), "personal must be an instance of Personal"
        assert isinstance(education, Education), "education must be an Education object"
        assert isinstance(
            work_history,
            WorkHistory,
        ), "work_history must be an instance of WorkHistory"
        assert isinstance(certifications, list), "certifications must be a list"
        assert all(
            isinstance(cert, Certification) for cert in certifications
        ), "certifications must be a list of Certification objects"

        self.personal = personal
        self.education = education
        self.work_history = work_history
        self.certifications = certifications

    @property
    def years_of_experience(self) -> int:
        """Return the number of years of experience."""

        _total_duration = timedelta()

        _date_ranges = []
        for _role in self.work_history.roles:
            _end_date = datetime.now() if _role.end_date is None else _role.end_date  # noqa: DTZ005

            _date_ranges.append((_role.start_date, _end_date))

        _merged_ranges = self._merge_date_ranges(_date_ranges)

        _total_days = 0

        for _start, _end in _merged_ranges:
            _total_days += (_end - _start).days

        _total_duration = round(_total_days / 365, 1)

        assert _total_duration >= 0, "_total_experience must be greater than 0"
        return _total_duration

    def _merge_date_ranges(
        self,
        date_ranges: list[tuple[datetime, datetime]],
    ) -> list[tuple[datetime, datetime]]:
        _sorted_ranges = sorted(date_ranges, key=lambda x: x[0])
        _merged_ranges = []

        _current_start_date, _current_end_date = _sorted_ranges[0]

        for _start, _end in _sorted_ranges[1:]:
            if _start <= _current_end_date:  # overlapping
                _current_end_date = max(_current_end_date, _end)
            else:
                _merged_ranges.append((_current_start_date, _current_end_date))
                _current_start_date, _current_end_date = _start, _end
        _merged_ranges.append((_current_start_date, _current_end_date))
        return _merged_ranges

    @property
    def career_experience(self) -> float:
        """Return the total number of years of experience."""

        _start_dates = [x.start_date for x in self.work_history.roles]
        _end_dates = [x.end_date for x in self.work_history.roles]

        _first_start_date = min(_start_dates)
        _last_end_date = max(_end_dates)

        # Calculate the total number of years of experience
        _total_career_experience = round(
            (_last_end_date - _first_start_date).days / 365,
            1,
        )
        return _total_career_experience

    def stats(self) -> dict[str, int]:
        """Return a dictionary of statistics about the resume."""

        return {
            "education": len(self.education.degrees),
            "roles": len(self.work_history.roles),
            "certifications": len(self.certifications),
            "total_experience": self.years_of_experience,
            "career_experience": self.career_experience,
        }
