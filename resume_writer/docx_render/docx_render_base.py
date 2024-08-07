class DocxRenderBase:
    """Base class for rendering docx files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    """

    def __init__(self):
        """Initialize superclass."""
        self.errors = []
        self.warnings = []
