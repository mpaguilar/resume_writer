import logging
from typing import TypeVar

T = TypeVar("T")

log = logging.getLogger(__name__)


class ParseError(Exception):
    """Exception raised when parsing fails."""


class ParseContext:
    """Tracking context while parsing."""

    def __init__(self, lines: list[str]):
        """Initialize ParseContext class instance."""

        assert isinstance(lines, list), "lines should be a list"

        self.lines = lines
        self.line_num = 0

    def __iter__(self):
        """Return iterator."""
        return self

    def __next__(self) -> str:
        """Return next line."""
        if self.line_num >= len(self.lines):
            raise StopIteration
        _line = self.lines[self.line_num]
        self.line_num += 1
        return _line

    def __getitem__(self, line_number: int) -> str:
        """Return line at line_number."""
        return self.lines[line_number - 1]


class ListBlockParse:
    """Mixin for parsing bullet points into a list."""

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the bullet list into lines of text."""

        assert isinstance(block_lines, list), "block_lines should be a list"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "All elements in block_lines should be strings"

        _items = []

        for _block_line in block_lines:
            # skip empty lines
            if not _block_line:
                continue

            if _block_line.startswith(("* ", "- ")):
                _line = _block_line[2:].strip()
                if _line == "":
                    continue
                _items.append(_block_line[2:])
            else:
                log.info(f"Skipping line: {_block_line}")

        assert all(item != "" for item in _items), "All items should be strings"

        return cls(_items)


class TextBlockParse:
    """Mixin for parsing blocks of text."""

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the block of lines into an object."""
        _lines = "\n".join(block_lines)
        # remove trailing newlines
        _lines = _lines.rstrip()

        # remove leading newlines
        _lines = _lines.lstrip()
        return cls(_lines)


class LabelBlockParse:
    """Mixin for parsing blocks for labels.

    Inheriting classes must implement `expected_fields` method, which
    is a mapping between the label and the argument name for the
    constructor.

    Example:
    -------
    @staticmethod
    def expected_fields() -> dict[str, str]:
        return {
            "school": "school",
            "degree": "degree",
            "start date": "start_date",
            "end date": "end_date",
        }

    """

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the block of lines into an object."""

        assert isinstance(block_lines, list)
        assert all(isinstance(line, str) for line in block_lines)

        _expected_fields = cls.expected_fields()
        _init_kwargs: dict[str, str | bool] = {}

        for _block_line in block_lines:
            # skip empty lines
            if not _block_line:
                continue

            _line_split = _block_line.split(":")
            # the line is just a line, not a label
            if len(_line_split) < 2:  # noqa: PLR2004
                continue

            _label = _line_split[0].lower()  # for lookup

            _user_label = _block_line.split(":")[0]  # verbatim

            # lookup the label in the expected fields
            if _label in _expected_fields:
                # the argument name is the value of the label in the expected fields
                _init_arg = _expected_fields[_label]
                # remove the label from the line, leaving the value
                _value = _block_line.replace(f"{_user_label}:", "", 1).strip()
                # if the value is empty, skip it
                if _value == "":
                    continue
                # add the argument name and value to the init kwargs
                _init_kwargs[_init_arg] = _value
                # remove the label from the expected fields
                _expected_fields.pop(_label)
            else:
                log.info(f"Skipping line: {_block_line}")

        # if there are any expected fields left, add them to the init kwargs with None
        _none_kwargs = {_field: None for _field in _expected_fields.values()}
        # update the init kwargs with the none kwargs
        _init_kwargs.update(_none_kwargs)

        return cls(**_init_kwargs)


class BasicBlockParse:
    """Mixin for blocks containing a mix of top level blocks.

    Subclasses must include two static methods:
    * `expected_blocks`: a dictionary of block names and their init arg names
    * `block_classes`: a dictionary of block names and the class to instanciate
    for that block.

    Example:
    -------
    @staticmethod
    def expected_blocks() -> dict[str, str]:
        return {
            "basics": "basics",
            "description": "description",
            "responsibilities": "responsibilities",
            "skills": "skills",
        }

    @staticmethod
    def block_classes() -> dict[str, type]:
        return {
            "basics": RoleBasics,
            "description": RoleDescription,
            "responsibilities": RoleResponsibilities,
            "skills": RoleSkills,
        }

    """

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
            # keep carriage returns, but strip everything else

            _block_line = _block_line.strip(" ")

            # if the line starts with "# ", it's a section header
            if _block_line.startswith("# "):
                _section_header = _block_line[1:].strip().lower()
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
    def kwargs_parse(cls: T, block_lines: list[str]) -> dict[str, str]:
        """Parse the block of lines into an dict.

        Use this when more processing has to be done.
        """
        _expected_blocks = cls.expected_blocks()
        _init_classes = cls.block_classes()
        _blocks: dict[str, str] = cls.parse_blocks(block_lines)

        _init_kwargs: dict[str, str] = {}
        for _block in _blocks:
            _lookup_block = _block.lower().strip()
            if _lookup_block in _expected_blocks and _lookup_block in _init_classes:
                _init_arg = _expected_blocks[_lookup_block]
                _init_kwargs[_init_arg] = _init_classes[_block].parse(_blocks[_block])
                _expected_blocks.pop(_lookup_block)
            else:
                log.info(f"Unexpected block: {_block}")

        _none_kwargs = {_field: None for _field in _expected_blocks.values()}
        _init_kwargs.update(_none_kwargs)
        return _init_kwargs

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the block of lines into an object."""
        _init_kwargs = cls.kwargs_parse(block_lines)

        return cls(**_init_kwargs)


class MultiBlockParse:
    """Mixin for blocks containing multiple blocks with the same name."""

    @classmethod
    def parse_blocks(cls: T, block_lines: list[str]) -> list[list[str]]:
        """Parse the block of lines into a list of blocks.

        Requires a static method named `list_class` which returns
        the `type` of the list items.

        """

        assert isinstance(block_lines, list), "Expected 'lines' to be of type list[str]"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "Expected all elements in 'lines' to be of type str"

        _blocks = []
        _current_block = []
        _section_header = None

        for _line in block_lines:

            # skip empty lines
            if not _line:
                continue

            if _line.startswith("# "):
                _section_header = _line[1:].strip().lower()
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

    @classmethod
    def parse(cls: T, block_lines: list[str]) -> T:
        """Parse the blocks and return a list of objects."""

        assert isinstance(block_lines, list), "Expected 'lines' to be of type list[str]"
        assert all(
            isinstance(line, str) for line in block_lines
        ), "Expected all elements in 'block_lines' to be of type str"


        log.debug(f"Parsing {len(block_lines)} block lines for {cls.__name__}")

        _object_list: list[cls] = []
        _object_blocks = cls.parse_blocks(block_lines)
        _list_type = cls.list_class()

        for _block in _object_blocks:
            _object = _list_type.parse(_block)
            _object_list.append(_object)

        log.debug(f"Parsed {len(_object_list)} objects for type {type(T)}")

        assert all(isinstance(obj, _list_type) for obj in _object_list)
        _new_obj = cls(_object_list)
        assert isinstance(_new_obj, cls)
        return _new_obj
