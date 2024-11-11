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

    def add_text(
        self,
        text: str,
        line_breaks: Literal["preserve", "strip"] = "preserve",
    ) -> None:
        """Add text to a Markdown document.

        Parameters
        ----------
        text : str
            The text to be added to the Markdown document.
        line_breaks : {'preserve', 'strip'}, optional
            Determines how line breaks are handled in the text. If 'strip',
            consecutive line breaks are reduced to a single line break. If
            'preserve', all line breaks in the text are preserved.
            Default is 'strip'.

        Returns
        -------
        None

        Notes
        -----
        1. The input text is split into lines.
        2. Each line is processed to remove any newline characters.
        3. If the line is empty and line_breaks is 'strip', the line is skipped.
        4. If the line starts with '#', it is treated as a header. Headers are
        separated by an additional newline for better formatting.
        5. The processed line is added to the Markdown document's text.
        6. The state of the previous line being a header is updated.

        """

        assert isinstance(text, str)
        assert isinstance(line_breaks, str)
        assert line_breaks in ("preserve", "strip")

        _lines = text.split("\n")
        _all_text = ""
        for _line in _lines:
            _text = re.sub("\n", "", _line)
            if not _text and line_breaks == "strip":
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
