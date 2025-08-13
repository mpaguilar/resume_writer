import re


class MarkdownDoc:
    """Represents a Markdown document used for generating and managing markdown content.

    Attributes:
        text (str): The current content of the markdown document, accumulated as text is added.
    """

    def __init__(self):
        """Initialize an empty Markdown document.

        Notes:
            1. Initializes the internal `text` attribute as an empty string.
        """
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add formatted text to the Markdown document.

        Args:
            text (str): The text to be added to the document. This may include markdown formatting such as headers.

        Returns:
            None

        Notes:
            1. Strips leading and trailing whitespace from the input text.
            2. If the text starts with a '#' (indicating a heading), adds a newline before and after the text to ensure proper formatting in the document.
            3. Appends the processed text to the document's internal `text` attribute.
            4. No disk, network, or database access is performed.
        """
        _text = re.sub(r"^\n+|\n+$", "", text)
        if _text.startswith("#"):
            _text = "\n" + _text + "\n"
        self.text += _text
