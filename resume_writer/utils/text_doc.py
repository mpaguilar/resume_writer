import re
from abc import ABC, abstractmethod
from typing import Literal


class TextDoc(ABC):
    """Base class for text documents.

    This abstract base class provides a common interface for different types of text documents.
    It defines the contract for adding text to a document through the `add_text` method.

    Attributes:
        None
    """

    @abstractmethod
    def add_text(self, text: str, **kwargs) -> None:  # noqa: ANN003
        """Provide abstract method for `add_text` interface.

        This method is intended to be implemented by subclasses to add text to the document.

        Args:
            text: The text to be added to the document.
            **kwargs: Additional keyword arguments that may be used by subclasses to customize behavior.

        Returns:
            None: This method does not return any value.

        Notes:
            1. This method is abstract and must be implemented by subclasses.
        """


class MarkdownDoc(TextDoc):
    """Markdown document.

    This class represents a document that follows Markdown formatting rules.
    It supports adding text and headers while managing line breaks and formatting.

    Attributes:
        text (str): The current content of the document as a string.
        previous_line_was_header (bool): Flag indicating whether the previous line was a header.
        first_line (bool): Flag indicating whether this is the first line being added to the document.
    """

    def __init__(self):
        """Initialize Markdown document.

        Initializes the text content to an empty string and sets flags to track the document state.
        """
        self.text: str = ""
        self.previous_line_was_header = False
        self.first_line = True

    def add_text(
        self,
        text: str,
        line_breaks: Literal["preserve", "strip"] = "strip",
    ) -> None:
        """Add text to a Markdown document.

        Processes the input text and appends it to the document with appropriate formatting.
        Handles line breaks based on the specified mode.

        Args:
            text: The text to be added to the document.
            line_breaks: Controls how line breaks in the input text are handled.
                - "preserve": Retains all line breaks as-is.
                - "strip": Removes blank lines and collapses multiple line breaks.

        Returns:
            None: This method modifies the internal state of the object.

        Notes:
            1. The input text is split into lines using `\n`.
            2. Each line is stripped of newline characters.
            3. If `line_breaks` is "strip" and the line is empty, it is skipped.
            4. The processed line is appended with a newline.
            5. If the previous line was a header, a blank line is added before the new text.
            6. The `previous_line_was_header` flag is updated after processing.
            7. The `first_line` flag is updated to False after the first addition.
            8. The processed text is appended to the document's `text` attribute.
        """
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
        """Add a markdown header.

        Adds a header line to the document. Ensures proper spacing before the header if needed.

        Args:
            header: The text to be used as the header.

        Returns:
            None: This method modifies the internal state of the object.

        Notes:
            1. If this is not the first line, a blank line is added before the header.
            2. The header is added to the document with a newline.
            3. The `previous_line_was_header` flag is set to True.
            4. The `first_line` flag is updated to False.
        """


class HtmlDoc(TextDoc):
    """HTML document.

    This class represents an HTML document that supports adding raw HTML text.
    It does not perform any parsing or formatting; it appends text as-is.

    Attributes:
        text (str): The current content of the HTML document as a string.
    """

    def __init__(self):
        """Initialize HTML document.

        Initializes the text content to an empty string.
        """
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to the HTML document.

        Appends the provided text to the existing content of the HTML document.

        Args:
            text: The text to be added to the HTML document.

        Returns:
            None: This method modifies the internal state of the object by appending the input text.

        Notes:
            1. The input text is appended directly to the document's `text` attribute.
            2. No formatting, validation, or transformation is applied to the input.
            3. This method performs no disk, network, or database access.
        """
        self.text += text
