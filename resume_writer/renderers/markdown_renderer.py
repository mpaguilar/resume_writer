import logging
from pathlib import Path

from resume_writer.models.resume import Resume
from resume_writer.resume_render.markdown.resume_main import RenderResume
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderResumeMarkdown:
    """Render a resume in Markdown format using Jinja templates.

    This class orchestrates the rendering process by initializing a Jinja environment
    with custom filters and delegating the actual rendering to a RenderResume instance.

    Attributes:
        resume (Resume): The resume data to be rendered.
        settings (ResumeRenderSettings): The settings for rendering the resume.
        renderer (RenderResume): The renderer responsible for generating the Markdown output.
        rendered (bool): Flag indicating whether the resume has been rendered.
    """

    def __init__(self, resume: Resume, settings: ResumeRenderSettings) -> None:
        """Initialize the MarkdownRenderer object.

        Parameters
        ----------
        resume : Resume
            The resume data to be rendered.
        settings : ResumeRenderSettings
            The settings for rendering the resume.

        Notes
        -----
        1. Validate that the provided resume is an instance of Resume.
        2. Validate that the provided settings is an instance of ResumeRenderSettings.
        3. Store the resume and settings data.
        4. Initialize the Markdown renderer.
        """
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings)

        self.resume = resume
        self.settings = settings
        self.renderer = self.init_renderer()
        self.rendered = False

    def init_renderer(self) -> RenderResume:
        """Initialize and return a RenderResume object.

        Returns
        -------
        RenderResume
            Initialized RenderResume object.

        Notes
        -----
        1. Create an instance of MarkdownDoc.
        2. Create a RenderResume object with the MarkdownDoc, resume data, and settings.
        3. Return the RenderResume object.
        """
        _document: MarkdownDoc = MarkdownDoc()
        assert isinstance(
            _document,
            MarkdownDoc,
        ), "Expected _document to be an instance of MarkdownDoc"

        _renderer = RenderResume(
            document=_document,
            resume=self.resume,
            settings=self.settings,
        )
        assert isinstance(
            _renderer,
            RenderResume,
        ), "Expected _renderer to be an instance of RenderResume"

        assert isinstance(self.resume, Resume), "Expected self.resume to be a Resume"
        assert isinstance(
            self.settings,
            ResumeRenderSettings,
        ), "Expected self.settings to be a ResumeRenderSettings"

        return _renderer

    def render(
        self,
    ) -> str:
        """Render the resume using the Markdown renderer.

        Returns
        -------
        str
            The rendered resume as a string.

        Notes
        -----
        1. Logs an info message indicating the start of the Markdown resume rendering.
        2. Calls the render method of the Markdown renderer.
        3. Sets the rendered attribute to True.
        4. Logs an info message indicating the completion of the Markdown resume rendering.
        """
        log.info("Rendering Markdown resume")

        self.renderer.render()

        self.rendered = True

        log.info("Render of Markdown resume complete.")

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
        5. Writes the rendered content to disk at the specified path.
        """
        assert isinstance(path, Path)

        if not self.rendered:
            log.warning("Resume not rendered. Call `render()` first.")
            return

        log.debug(f"Saving Markdown resume to {path}")
        self.renderer.save(path)
        log.info(f"Saved Markdown resume to {path}")

    def content(self) -> str:
        """Return the rendered content of the resume.

        This method should be called after the `render()` method.

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
