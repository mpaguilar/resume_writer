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
    """Render Education Section."""

    def __init__(
        self,
        document: MarkdownDoc,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic education renderer."""
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
        ), f"Expected settings to be of type ResumeEducationSettings, but got {type(settings)}"  # noqa: E501

        super().__init__(
            document=document,
            education=education,
            template_name="",
            jinja_env=None,
            settings=settings,
        )

    def render_degree(self, degree: Degree) -> None:
        """Render a single degree."""
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
        """Render the education section."""
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
