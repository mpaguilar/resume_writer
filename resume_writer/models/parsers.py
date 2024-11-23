import logging
from typing import TypeVar

T = TypeVar("T")

log = logging.getLogger(__name__)


class ParseError(Exception):
    """Exception raised when parsing fails."""

    def __init__(self, message: str, parse_context: "ParseContext"):
        """Initialize ParseError class instance, add parse_context info to message."""

        _start_line = parse_context.doc_line_num - parse_context.line_num
        _msg = f"{message} (lines {_start_line}-{parse_context.doc_line_num})"
        super().__init__(_msg)


class ParseContext:
    """Tracking context while parsing."""

    def __init__(self, lines: list[str], doc_line_num: int):
        """Initialize ParseContext class instance."""

        assert isinstance(lines, list), "lines should be a list"

        self.lines = lines
        self.line_num = 1
        self.doc_line_num = doc_line_num

    def __iter__(self):
        """Return iterator."""
        return self

    def __next__(self) -> str:
        """Return next line."""
        if self.line_num >= len(self.lines) + 1:
            raise StopIteration

        # humans start at line 1, but python starts at line 0
        _line = self.lines[self.line_num - 1]
        self.line_num += 1
        self.doc_line_num += 1
        return _line

    def __len__(self) -> int:
        """Return number of lines in the context."""
        return len(self.lines)

    def append(self, line: str) -> None:
        """Add a line to the list of lines."""
        assert isinstance(line, str), "line should be a string"
        self.lines.append(line)

    def clear(self) -> None:
        """Clear the list of lines."""
        self.lines.clear()
        self.line_num = 1


class ListBlockParse:
    """Mixin for parsing bullet points into a list."""

    @classmethod
    def parse(cls: T, parse_context: ParseContext) -> T:
        """Parse the bullet list into lines of text."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        _items = []

        for _block_line in parse_context:
            # skip empty lines
            if not _block_line:
                continue

            if _block_line.startswith(("* ", "- ")):
                _line = _block_line[2:].strip()
                if _line == "":
                    continue
                _items.append(_block_line[2:])
            elif _block_line.strip():
                log.info(f"Skipping line: {_block_line.strip()}")
            else:
                log.info(f"Skipping line: {_block_line}")

        assert all(item != "" for item in _items), "All items should be strings"

        return cls(_items, parse_context=parse_context)


class TextBlockParse:
    """Mixin for parsing blocks of text."""

    @classmethod
    def parse(cls: T, parse_context: ParseContext) -> T:
        """Parse the block of lines into an object."""

        _block_lines = []
        for _line in parse_context:
            _block_lines.append(_line)  # noqa: PERF402

        _lines = "\n".join(_block_lines)
        # remove trailing newlines
        _lines = _lines.rstrip()

        # remove leading newlines
        _lines = _lines.lstrip()
        return cls(parse_context=parse_context, text_string=_lines)


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
    def parse(cls: T, parse_context: ParseContext) -> T:
        """Parse the block of lines into an object."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        _expected_fields = cls.expected_fields()
        _init_kwargs: dict[str, str | bool] = {}

        for _block_line in parse_context:
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
            elif _block_line.strip():
                log.info(f"Skipping line: {_block_line.strip()}")
            else:
                log.info(f"Skipping line: {_block_line}")

        # if there are any expected fields left, add them to the init kwargs with None
        _none_kwargs = {_field: None for _field in _expected_fields.values()}
        # update the init kwargs with the none kwargs
        _init_kwargs.update(_none_kwargs)
        _init_kwargs["parse_context"] = parse_context

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
    def parse_blocks(cls: T, parse_context: ParseContext) -> dict[str, str]:
        """Parse the block of lines into a dictionary of blocks."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        _blocks: dict = {}

        _section_header = None

        # iterate over the lines in the block
        for _block_line in parse_context:
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
                _blocks[_section_header] = ParseContext(
                    lines=[],
                    doc_line_num=parse_context.doc_line_num,
                )
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
                    log.debug(f"Found subheader: {_block_line.strip()}")
                _blocks[_section_header].append(_block_line)

        # check up on the values we've got so far
        assert isinstance(_blocks, dict), "_blocks should be a dictionary"
        assert all(
            isinstance(key, str) for key in _blocks
        ), "_blocks keys should be strings"
        assert all(
            isinstance(value, ParseContext) for value in _blocks.values()
        ), "_blocks values should be ParseContext"

        return _blocks

    @classmethod
    def kwargs_parse(cls: T, parse_context: ParseContext) -> dict[str, str]:
        """Parse the block of lines into an dict.

        Use this when more processing has to be done.
        """

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        _expected_blocks = cls.expected_blocks()
        _init_classes = cls.block_classes()
        _blocks: dict[str, str] = cls.parse_blocks(parse_context=parse_context)

        _init_kwargs: dict[str, str] = {}
        for _block in _blocks:
            _lookup_block = _block.lower().strip()
            if _lookup_block in _expected_blocks and _lookup_block in _init_classes:
                _init_arg = _expected_blocks[_lookup_block]
                _init_kwargs[_init_arg] = _init_classes[_block].parse(
                    _blocks[_block],
                )
                _expected_blocks.pop(_lookup_block)
            else:
                log.info(f"Unexpected block: {_block}")

        _none_kwargs = {_field: None for _field in _expected_blocks.values()}
        _init_kwargs.update(_none_kwargs)
        _init_kwargs["parse_context"] = parse_context
        return _init_kwargs

    @classmethod
    def parse(cls: T, parse_context: ParseContext) -> T:
        """Parse the block of lines into an object."""
        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"
        _init_kwargs = cls.kwargs_parse(parse_context=parse_context)

        return cls(**_init_kwargs)


class MultiBlockParse:
    """Mixin for blocks containing multiple blocks with the same name."""

    @classmethod
    def parse_blocks(cls: T, parse_context: ParseContext) -> list[list[str]]:
        """Parse the block of lines into a list of blocks.

        Requires a static method named `list_class` which returns
        the `type` of the list items.

        """

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        _blocks = []
        _current_block = ParseContext(lines=[], doc_line_num=parse_context.doc_line_num)
        _section_header = None

        for _line in parse_context:
            # skip empty lines
            if not _line:
                continue

            if _line.startswith("# "):
                _section_header = _line[1:].strip().lower()
                log.info(f"Found section header: {_section_header}")
                if len(_current_block) > 0:
                    _blocks.append(_current_block)
                _current_block = ParseContext(
                    lines=[],
                    doc_line_num=parse_context.doc_line_num,
                )
                continue

            if _section_header is not None:
                if _line.startswith("#"):
                    # this is a subheader, we want the line, but not the extra level
                    _line = _line[1:]
                _current_block.append(_line)

        # Get the last block
        if len(_current_block) > 0:
            _blocks.append(_current_block)

        assert isinstance(
            _blocks,
            list,
        ), "Expected '_blocks' to be of type list[ParseContext]"
        assert all(
            isinstance(block, ParseContext) for block in _blocks
        ), "Expected all elements in '_blocks' to be of type ParseContext"

        return _blocks

    @classmethod
    def parse(cls: T, parse_context: ParseContext) -> T:
        """Parse the blocks and return a list of objects."""

        assert isinstance(
            parse_context,
            ParseContext,
        ), "parse_context must be a ParseContext"

        log.debug(f"Parsing {len(parse_context)} block lines for {cls.__name__}")

        _object_list: list[cls] = []
        _object_blocks = cls.parse_blocks(parse_context=parse_context)
        _list_type = cls.list_class()

        for _block in _object_blocks:
            _object = _list_type.parse(_block)
            _object_list.append(_object)

        log.debug(f"Parsed {len(_object_list)} objects for type {type(T)}")

        assert all(isinstance(obj, _list_type) for obj in _object_list)
        _new_obj = cls(_object_list, parse_context=parse_context)
        assert isinstance(_new_obj, cls)
        return _new_obj
