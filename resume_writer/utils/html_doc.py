class HtmlDoc:
    """HTML document."""

    def __init__(self):
        """Initialize HTML document."""
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to HTML document."""
        self.text += text
