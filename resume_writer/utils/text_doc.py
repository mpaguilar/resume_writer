import re
from abc import ABC, abstractmethod
from typing import Literal


class TextDoc(ABC):
    """Base class for text documents."""

    @abstractmethod
    def add_text(self, text: str, **kwargs) -> None:  # noqa: ANN003
        """Provide abstract method for `add_text` interface."""


class MarkdownDoc(TextDoc):
    """Markdown document."""

    def __init__(self):
        """Initialize Markdown document."""
        self.text: str = ""
        self.previous_line_was_header = False
        self.first_line = True

    def add_text(
        self,
        text: str,
        line_breaks: Literal["preserve", "strip"] = "strip",
    ) -> None:
        """Add text to a Markdown document."""

        assert isinstance(text, str)
        assert isinstance(line_breaks, str)
        assert line_breaks in ("preserve", "strip")

        _lines = text.split("\n")
        _all_text = ""

        if self.previous_line_was_header:
            _all_text += "\n"

        for _line in _lines:
            _text = re.sub("\n", "", _line)
            if not _text and line_breaks == "strip":
                continue

            _all_text += _text + "\n"

        self.previous_line_was_header = False
        self.first_line = False

        self.text += _all_text

    def add_header(self, header: str) -> None:
        """Add a markdown header."""

        if not self.first_line:
            self.text += "\n"

        self.text += f"{header}\n"

        self.previous_line_was_header = True
        self.first_line = False


class HtmlDoc(TextDoc):
    """HTML document."""

    def __init__(self):
        """Initialize HTML document."""
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to the HTML document.

        Parameters
        ----------
        text : str
            The text to be added to the HTML document.

        Returns
        -------
        None
            This method does not return any value. It modifies the
            internal state of the object by appending the input text
            to the existing text in the HTML document.

        Notes
        -----
        1. This method takes a string as input.
        2. The input string is appended to the existing text in the
        HTML document.
        3. This method does not return any value. It modifies the
        internal state of the object.

        """
        self.text += text
