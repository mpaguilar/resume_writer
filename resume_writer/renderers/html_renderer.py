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
    """Render a resume to HTML format using Jinja2 templates.

    This class coordinates the rendering process by initializing the Jinja2 environment,
    managing the rendering pipeline, and saving the final output.

    Attributes:
        jinja_env (Environment): The Jinja2 environment configured with custom filters.
        resume (Resume): The resume data to be rendered.
        settings (ResumeRenderSettings): Configuration settings for rendering.
        renderer (RenderResume): The underlying renderer responsible for generating HTML.
        rendered (bool): Flag indicating whether the resume has been rendered.
    """

    def __init__(self, resume: Resume, settings: ResumeRenderSettings) -> None:
        """Initialize the HTMLRenderer object.

        Args:
            resume (Resume): The resume data to be rendered.
            settings (ResumeRenderSettings): The settings for rendering the resume.

        Notes:
            1. Validates that resume is an instance of Resume and settings is an instance of ResumeRenderSettings.
            2. Initializes the Jinja2 environment.
            3. Stores the resume and settings data.
            4. Initializes the HTML renderer.
            5. Sets the rendered flag to False.
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

        Returns:
            RenderResume: Initialized RenderResume object.

        Notes:
            1. Creates an instance of HtmlDoc.
            2. Creates a RenderResume object with the HtmlDoc, Jinja environment, resume data, and settings.
            3. Returns the RenderResume object.
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
        """Initialize the Jinja environment with custom filters.

        Returns:
            Environment: The initialized Jinja environment.

        Notes:
            1. Defines a date filter function to format dates in the Jinja template.
            2. Defines a line feed to HTML break function to convert line feeds to HTML breaks.
            3. Defines a list length function to calculate the length of a list.
            4. Initializes the Jinja environment with the custom filters.
            5. Loads templates from the 'resume_writer.resume_render.html' package.
            6. Enables autoescaping for HTML output.
        """
        def date_filter(resdate: datetime | None, date_format: str = "%B %Y") -> str:
            """Format dates in Jinja template.

            Args:
                resdate (datetime | None): The date to format.
                date_format (str, optional): The format string for the date. Defaults to "%B %Y".

            Returns:
                str: The formatted date string or "Present" if resdate is None.

            Notes:
                1. Validates that resdate is either a datetime object or None.
                2. Validates that date_format is a string.
                3. Returns "Present" if resdate is None.
                4. Otherwise, formats the date using strftime with the specified format.
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

            Notes:
                1. Validates that text is a string.
                2. Replaces "\r\n" with "\n".
                3. Replaces "\n\n" with "\n".
                4. Replaces "\n" with "<br>".
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

            Notes:
                1. Validates that lst is a list.
                2. Returns the length of the list using len().
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

        Returns:
            str: The rendered resume as a string.

        Notes:
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

        Args:
            path (Path): The path where the resume will be saved.

        Raises:
            AssertionError: If the provided path is not an instance of Path.

        Notes:
            1. Checks if the provided path is an instance of Path.
            2. Checks if the resume has been rendered. If not, logs a warning and returns.
            3. Logs a debug message indicating the save location.
            4. Calls the renderer's save method to save the resume to the file.
            5. Logs an info message indicating the successful save.
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

        Returns:
            str: The rendered content of the resume as a string.

        Notes:
            1. Checks if the resume has been rendered.
            2. If not, logs a warning message and returns an empty string.
            3. If yes, returns the rendered content as a string.
        """
        if not self.rendered:
            log.warning("Resume not rendered. Call `render()` first.")
            return ""

        return self.renderer.document.text
