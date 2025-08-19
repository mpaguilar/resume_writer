import logging
from typing import TypeVar

T = TypeVar("T")

log = logging.getLogger(__name__)


class ParseError(Exception):
    """Exception raised when parsing fails.

    Args:
        message: A human-readable description of the parsing error.
        parse_context: The current context of the parsing operation, used to track line numbers.

    Returns:
        None. This exception is raised to signal a parsing failure.

    Notes:
        1. The error message is enhanced with the line range (start-end) of the failure.
        2. The line range is derived from the parse_context's doc_line_num and the initial line number.
        3. The exception is initialized with the enriched message, which includes the line range.

    """


class ParseContext:
    """Tracking context while parsing.

    Attributes:
        lines (list[str]): The list of lines to be parsed.
        line_num (int): The current line number in the parsing process (1-indexed).
        doc_line_num (int): The current line number in the original document.

    Args:
        lines: A list of strings representing the lines to be parsed.
        doc_line_num: The current line number in the document (used for tracking).

    Returns:
        An initialized ParseContext object.

    Notes:
        1. The input lines are validated to ensure they are a list.
        2. The line_num is initialized to 1 (human-readable line numbering).
        3. The doc_line_num is initialized to the provided value.
        4. The ParseContext supports iteration using __iter__ and __next__.
        5. The __next__ method returns one line at a time, advancing line_num and doc_line_num.
        6. The __len__ method returns the number of lines in the context.
        7. The append method adds a string to the lines list.
        8. The clear method empties the lines list and resets line_num.

    """

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
    """Mixin for parsing bullet points into a list.

    Args:
        parse_context: The current parsing context, containing lines to parse.

    Returns:
        An instance of the class with parsed items.

    Notes:
        1. The parse_context is validated to ensure it is a ParseContext.
        2. An empty list _items is initialized to store parsed items.
        3. Each line in the parse_context is processed:
            a. Empty lines are skipped.
            b. Lines starting with "* " or "- " are split into a label and value.
            c. The label is discarded, and the value is added to _items if not empty.
            d. Other non-empty lines are logged as skipped.
        4. All items in _items must be non-empty strings.
        5. The parsed list is returned as an instance of the class.

    """

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
    """Mixin for parsing blocks of text.

    Args:
        parse_context: The current parsing context, containing lines to parse.

    Returns:
        An instance of the class with the concatenated and cleaned text.

    Notes:
        1. The parse_context is validated to ensure it is a ParseContext.
        2. An empty list _block_lines is initialized to collect lines.
        3. Each line in the parse_context is added to _block_lines.
        4. The lines are joined with newlines and stripped of leading/trailing whitespace.
        5. The resulting string is returned as an instance of the class.

    """

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

    Args:
        parse_context: The current parsing context, containing lines to parse.

    Returns:
        An instance of the class with parsed fields.

    Notes:
        1. The parse_context is validated to ensure it is a ParseContext.
        2. A dictionary _expected_fields is retrieved from the class's expected_fields method.
        3. A dictionary _init_kwargs is initialized to store parsed field values.
        4. Each line in the parse_context is processed:
            a. Empty lines are skipped.
            b. Lines not containing a colon are skipped.
            c. The label part is extracted and converted to lowercase for lookup.
            d. If the label is in _expected_fields, the value is extracted, and the key-value pair is added to _init_kwargs.
            e. If the value is empty, it is skipped.
            f. Other non-empty lines are logged as skipped.
        5. Remaining keys in _expected_fields are added to _init_kwargs with None values.
        6. The parse_context is added to _init_kwargs.
        7. The class is instantiated with the populated _init_kwargs.

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

    Args:
        parse_context: The current parsing context, containing lines to parse.

    Returns:
        An instance of the class with parsed blocks.

    Notes:
        1. The parse_context is validated to ensure it is a ParseContext.
        2. A dictionary _blocks is initialized to store parsed blocks.
        3. A variable _section_header is initialized to track the current section.
        4. Each line in the parse_context is processed:
            a. If the line starts with "# ", it is a section header, and _section_header is set.
            b. If there is no section header yet, the line is logged as unexpected.
            c. If the line does not start with "#", it is added to the current section.
        5. The section header is used to store the block context.
        6. After processing, the block contexts are converted to blocks using parse_blocks.
        7. The kwargs_parse method is called to process the blocks.
        8. The class is instantiated with the parsed kwargs.

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
        assert all(isinstance(key, str) for key in _blocks), (
            "_blocks keys should be strings"
        )
        assert all(isinstance(value, ParseContext) for value in _blocks.values()), (
            "_blocks values should be ParseContext"
        )

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
                log.error(f"Unexpected block: {_block}")

        # if there are any expected blocks left, add them to the init kwargs with None
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
    """Mixin for blocks containing multiple blocks with the same name.

    Args:
        parse_context: The current parsing context, containing lines to parse.

    Returns:
        An instance of the class with a list of parsed objects.

    Notes:
        1. The parse_context is validated to ensure it is a ParseContext.
        2. A list _blocks is initialized to store parsed block contexts.
        3. A variable _current_block is initialized to collect lines for the current block.
        4. A variable _section_header is initialized to track the current section.
        5. Each line in the parse_context is processed:
            a. Empty lines are skipped.
            b. Lines starting with "# " are section headers, and _section_header is set.
            c. If a new section header is found and _current_block is non-empty, it is added to _blocks.
            d. If _section_header is set, the line is added to _current_block.
        6. After processing, the last _current_block is added to _blocks if non-empty.
        7. The block contexts in _blocks are validated.
        8. The list_class method is called to get the type of the list items.
        9. Each block context is parsed into an object using the list_class type.
        10. The list of objects is returned as an instance of the class.

    """

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
        assert all(isinstance(block, ParseContext) for block in _blocks), (
            "Expected all elements in '_blocks' to be of type ParseContext"
        )

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
