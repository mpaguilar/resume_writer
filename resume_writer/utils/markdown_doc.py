import re


class MarkdownDoc:
    """HTML document."""

    def __init__(self):
        """Initialize HTML document."""
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to HTML document."""
        _text = re.sub(r"^\n+|\n+$", "", text)
        if _text.startswith("#"):
            _text = "\n" + _text + "\n"
        self.text += _text
