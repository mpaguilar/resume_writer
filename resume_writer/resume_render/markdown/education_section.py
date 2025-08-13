import logging

from resume_writer.models.education import Degree, Education
from resume_writer.resume_render.render_settings import ResumeEducationSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderEducationBase,
)
from resume_writer.utils.date_format import format_date
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderEducationSection(ResumeRenderEducationBase):
    """Render Education Section.

    Attributes:
        document (MarkdownDoc): The Markdown document to which the education section will be added.
        education (Education): The Education object containing degree information to render.
        settings (ResumeEducationSettings): The settings object defining which fields to include in the rendered output.
    """

    def __init__(
        self,
        document: MarkdownDoc,
        education: Education,
        settings: ResumeEducationSettings,
    ) -> None:
        """Initialize the basic education renderer.

        Args:
            document (MarkdownDoc): The Markdown document to which rendered content will be added.
            education (Education): The Education object containing degree information to be rendered.
            settings (ResumeEducationSettings): The settings object defining which fields to render.

        Returns:
            None

        Notes:
            1. Validate that the provided document is an instance of MarkdownDoc.
            2. Validate that the provided education is an instance of Education.
            3. Validate that the provided settings is an instance of ResumeEducationSettings.
            4. Call the parent class constructor with the provided arguments.

        """
        assert isinstance(
            document,
            MarkdownDoc,
        ), f"Expected document to be of type MarkdownDoc, but got {type(document)}"
        assert isinstance(
            education,
            Education,
        ), f"Expected education to be of type Education, but got {type(education)}"
        assert isinstance(
            settings,
            ResumeEducationSettings,
        ), (
            f"Expected settings to be of type ResumeEducationSettings, but got {type(settings)}"
        )  # noqa: E501

        super().__init__(
            document=document,
            education=education,
            template_name="",
            jinja_env=None,
            settings=settings,
        )

    def render_degree(self, degree: Degree) -> None:
        """Render a single degree in the education section.

        Args:
            degree (Degree): The Degree object containing details such as school, degree, major, dates, and GPA.

        Returns:
            None

        Notes:
            1. Retrieve shortcuts for the document and settings.
            2. Add a header for the degree section with "### Degree".
            3. If the settings flag for school is enabled and the degree has a school, add the school to the document.
            4. If the settings flag for degree is enabled and the degree has a degree name, add the degree to the document.
            5. If the settings flag for major is enabled and the degree has a major, add the major to the document.
            6. If the settings flag for start_date is enabled and the degree has a start date, format and add the start date to the document.
            7. If the settings flag for end_date is enabled and the degree has an end date, format and add the end date to the document.
            8. If the settings flag for gpa is enabled and the degree has a GPA, add the GPA to the document.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings

        _doc.add_header("### Degree")

        if _settings.school and degree.school:
            _doc.add_text(f"School: {degree.school}")
        if _settings.degree and degree.degree:
            _doc.add_text(f"Degree: {degree.degree}")
        if _settings.major and degree.major:
            _doc.add_text(f"Major: {degree.major}")
        if _settings.start_date and degree.start_date:
            _doc.add_text(f"Start Date: {format_date(degree.start_date)}")
        if _settings.end_date and degree.end_date:
            _doc.add_text(f"End Date: {format_date(degree.end_date)}")
        if _settings.gpa and degree.gpa:
            _doc.add_text(f"GPA: {degree.gpa}")

    def render(self) -> None:
        """Render the complete education section.

        Args:
            None

        Returns:
            None

        Notes:
            1. Retrieve shortcuts for the document, settings, and education.
            2. If the settings flag for degrees is disabled, log a debug message and return.
            3. Log a debug message indicating that the education section is being rendered.
            4. Add a top-level header for the education section with "# Education".
            5. Add a sub-header for the degrees section with "## Degrees".
            6. Iterate over each degree in the education object and call render_degree for each.

        """
        # shortcuts
        _doc = self.document
        _settings = self.settings
        _education = self.education

        if not _settings.degrees:
            log.debug("No degrees to render.")
            return

        log.debug("Rendering education section.")

        _doc.add_header("# Education")
        _doc.add_header("## Degrees")

        for degree in _education.degrees:
            self.render_degree(degree)
