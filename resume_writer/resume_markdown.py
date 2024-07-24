import logging

import resume_model

log = logging.getLogger(__name__)


class MarkdownResumeParser:
    """Parse a markdown file into a Resume object."""

    def __init__(self, file_path: str):
        """Initialize the parser."""
        self.file_path = file_path

    def parse_personal_block(
        self,
        block_lines: list[str],
    ) -> resume_model.Personal:
        """Parse a block of personal information.

        Allowed headers:
        - Info
        - Banner
        - Note

        """
        _personal_info = resume_model.PersonalInfo()
        _banner = None
        _note = None

        _blocks = self.get_top_level_blocks(block_lines)
        for _block_name, _block_lines in _blocks.items():
            # Parse the block lines into a PersonalInfo object.
            if _block_name.lower() == "info":
                _name = ""
                _email = ""
                _phone = ""
                for _block_line in _block_lines:

                    if _block_line.lower().startswith("name:"):
                        _name = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("email:"):
                        _email = _block_line.split(":")[1].strip()
                    if _block_line.lower().startswith("phone:"):
                        _phone = _block_line.split(":")[1].strip()

                _personal_info = resume_model.PersonalInfo(
                    name=_name,
                    email=_email,
                    phone=_phone,
                )

            if _block_name.lower() == "banner":
                _banner = "".join(_block_lines)

            if _block_name.lower() == "note":
                _note = "".join(_block_lines)

        _personal = resume_model.Personal(
            personal_info=_personal_info,
            banner=_banner,
            note=_note,
        )

        return _personal

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

        _blocks = {}

        # break the lines into markdown sections by header
        for _line in lines:
            _line = _line.strip()

            # skip empty lines
            if not _line:
                continue

            # if the line starts with a '# ', it's a top-level header
            if _line.startswith("# "):
                _section_header = _line[1:].strip()
                log.debug(f"Found section header: {_section_header}")
                _blocks[_section_header] = []
                continue

            # if the line doesn't start with a #, it's a line of text
            if _line and not _line.startswith("# "):
                if _line.startswith("#"):
                    # this is a subheader, add it after removing the hash
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

        return _blocks
