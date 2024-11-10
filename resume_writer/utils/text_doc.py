import re
from abc import ABC, abstractmethod


class TextDoc(ABC):
    """Base class for text documents."""

    @abstractmethod
    def add_text(self, text: str) -> None:
        """Provide abstract method for `add_text` interface."""


class MarkdownDoc(TextDoc):
    """HTML document."""

    def __init__(self):
        """Initialize HTML document."""
        self.text: str = ""
        self.previous_line_was_header = False

    def add_text(self, text: str) -> None:
        """Add text to HTML document."""

        assert isinstance(text, str)

        _lines = text.split("\n")
        _all_text = ""
        for _line in _lines:
            _text = re.sub("\n", "", _line)
            if not _text:
                continue

            if _text.startswith("#"):
                if not self.previous_line_was_header:
                    _all_text += "\n"
                _all_text += _text + "\n\n"
                self.previous_line_was_header = True
            else:
                _all_text += _text + "\n"
                self.previous_line_was_header = False

        self.text += _all_text


class HtmlDoc(TextDoc):
    """HTML document."""

    def __init__(self):
        """Initialize HTML document."""
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to HTML document."""
        self.text += text
