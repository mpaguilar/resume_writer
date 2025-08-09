import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from resume_writer.models.resume import Resume
from resume_writer.resume_render.html.resume_main import RenderResume
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.utils.text_doc import HtmlDoc

log = logging.getLogger(__name__)


class RenderResumeHtml:
    """Initialize the Jinja environment.

    Steps:
    1. Define a date filter function to format dates in the Jinja template.
    2. Define a line feed to HTML break function to convert line feeds to HTML breaks.
    3. Define a list length function to calculate the length of a list.
    4. Initialize the Jinja environment with the custom filters.

    Returns:
        Environment: The initialized Jinja environment.

    """

    def __init__(self, resume: Resume, settings: ResumeRenderSettings) -> None:
        """Initialize the HTMLRenderer object.

        Parameters
        ----------
        resume : Resume
            The resume data to be rendered.
        settings : ResumeRenderSettings
            The settings for rendering the resume.

        Steps
        -----
        1. Initialize the Jinja environment.
        2. Store the resume and settings data.
        3. Initialize the HTML renderer.

        """
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings)

        self.jinja_env = self.init_jinja()
        self.resume = resume
        self.settings = settings
        self.renderer = self.init_renderer()
        self.rendered: bool = False

    def init_renderer(self) -> RenderResume:
        """Initialize and return a RenderResume object.

        Steps:
        1. Create an instance of HtmlDoc.
        2. Create a RenderResume object with the HtmlDoc,
        Jinja environment, resume data, and settings.
        3. Return the RenderResume object.

        Returns:
        RenderResume: Initialized RenderResume object.

        """
        _document: HtmlDoc = HtmlDoc()
        _renderer = RenderResume(
            document=_document,
            jinja_env=self.jinja_env,
            resume=self.resume,
            settings=self.settings,
        )
        return _renderer

    def init_jinja(self) -> Environment:
        """Initialize the Jinja environment.

        Steps:
        1. Define a date filter function to format dates in the Jinja template.
        2. Define a line feed to HTML break function to convert line feeds to HTML
            breaks.
        3. Define a list length function to calculate the length of a list.
        4. Initialize the Jinja environment with the custom filters.

        Returns:
            Environment: The initialized Jinja environment.

        """

        def date_filter(resdate: datetime | None, date_format: str = "%B %Y") -> str:
            """Format dates in Jinja template.

            Args:
                resdate (datetime | None): The date to format.
                date_format (str, optional): The format string for the date.
                    Defaults to "%B %Y".

            Returns:
                str: The formatted date string or "Present" if resdate is None.

            """
            assert isinstance(resdate, (datetime, type(None))), "Invalid datetime"
            assert isinstance(date_format, str), "Invalid date format"

            if resdate is None:
                return "Present"

            return resdate.strftime(date_format)

        def lf_to_br(text: str) -> str:
            """Convert line feeds to HTML breaks.

            Args:
                text (str): The input text.

            Returns:
                str: The input text with line feeds replaced by HTML breaks.

            """
            assert isinstance(text, str)
            _txt = text.replace("\r\n", "\n")
            _txt = _txt.replace("\n\n", "\n")
            _txt = _txt.replace("\n", "<br>")
            return _txt

        def list_len(lst: list) -> int:
            """Return the length of a list.

            Args:
                lst (list): The input list.

            Returns:
                int: The length of the list.

            """
            assert isinstance(lst, list)
            return len(lst)

        jinja_env = Environment(
            loader=PackageLoader("resume_writer.resume_render.html"),
            autoescape=select_autoescape(),
        )
        jinja_env.filters["date"] = date_filter
        jinja_env.filters["lf_to_br"] = lf_to_br
        jinja_env.filters["list_len"] = list_len

        return jinja_env

    def render(
        self,
    ) -> str:
        """Render the resume using the HTML renderer.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The rendered resume as a string.

        Notes
        -----
        1. Logs an info message indicating the start of the HTML resume rendering.
        2. Calls the render method of the HTML renderer.
        3. Sets the rendered attribute to True.
        4. Logs an info message indicating the completion of the HTML resume rendering.

        """
        log.info("Rendering HTML resume")

        self.renderer.render()

        self.rendered = True

        log.info("Render of HTML resume complete.")

    def save(self, path: Path) -> None:
        """Save the rendered resume to a file.

        Parameters
        ----------
        path : Path
            The path where the resume will be saved.

        Raises
        ------
        AssertionError
            If the provided path is not an instance of Path.

        Notes
        -----
        1. Check if the resume is rendered. If not, log a warning and return.
        2. Log a debug message indicating the save location.
        3. Call the renderer's save method to save the resume to the file.
        4. Log an info message indicating the successful save.

        """
        assert isinstance(path, Path)

        if not self.rendered:
            log.warning("Resume not rendered. Call `render()` first.")
            return

        log.debug(f"Saving HTML resume to {path}")
        self.renderer.save(path)
        log.info(f"Saved HTML resume to {path}")

    def content(self) -> str:
        """Return the rendered content of the resume.

        This method should be called after the `render()` method.

        Parameters
        ----------
        self : object
            Instance of the class.

        Returns
        -------
        str
            The rendered content of the resume as a string.

        Notes
        -----
        1. Checks if the resume has been rendered.
        2. If not, logs a warning message and returns an empty string.
        3. If yes, returns the rendered content as a string.

        """
        if not self.rendered:
            log.warning("Resume not rendered. Call `render()` first.")
            return ""

        return self.renderer.document.text
