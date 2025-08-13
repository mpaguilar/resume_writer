class HtmlDoc:
    """HTML document.

    Attributes:
        text (str): The HTML content of the document, accumulated through add_text calls.
    """

    def __init__(self):
        """Initialize HTML document.

        Notes:
            1. Initializes the text attribute to an empty string.
        """
        self.text: str = ""

    def add_text(self, text: str) -> None:
        """Add text to HTML document.

        Args:
            text (str): The text to append to the document. This text is added as-is to the HTML content.

        Returns:
            None: This function does not return a value.

        Notes:
            1. Concatenates the provided text to the existing document content.
            2. No disk, network, or database access occurs.
        """
        self.text += text
