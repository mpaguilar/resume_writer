import logging

from jinja2 import Environment

from resume_writer.models.education import Education
from resume_writer.resume_render.render_settings import ResumeEducationSettings
from resume_writer.resume_render.resume_render_text_base import (
    ResumeRenderEducationBase,
)
from resume_writer.utils.text_doc import MarkdownDoc

log = logging.getLogger(__name__)


class RenderEducationSection(ResumeRenderEducationBase):
    """Render Education Section."""

    def __init__(
        self,
        document: MarkdownDoc,
        jinja_env: Environment,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic education renderer."""
        assert isinstance(
            document,
            MarkdownDoc,
        ), f"Expected document to be of type MarkdownDoc, but got {type(document)}"
        assert isinstance(
            jinja_env,
            Environment,
        ), f"Expected jinja_env to be of type Environment, but got {type(jinja_env)}"
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
            jinja_env=jinja_env,
            education=education,
            template_name="education.j2",
            settings=settings,
        )

    def render_degree(self, degree) -> None:
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
        if _settings.gpa and degree.gpa:
            _doc.add_text(f"GPA: {degree.gpa}")
        if _settings.start_date and degree.start_date:
            _doc.add_text(f"Start Date: {degree.start_date}")
        if _settings.end_date and degree.end_date:
            _doc.add_text(f"End Date: {degree.end_date}")

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

