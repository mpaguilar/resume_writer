import logging

import docx.document
from resume_render.render_settings import ResumeEducationSettings
from resume_render.resume_render_base import (
    ResumeRenderDegreeBase,
    ResumeRenderEducationBase,
)

from resume_writer.models.education import Degree, Education

log = logging.getLogger(__name__)


class RenderDegreeSection(ResumeRenderDegreeBase):
    """Render Degree Section."""

    def __init__(
        self,
        document: docx.document.Document,
        degree: Degree,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic degree renderer."""
        super().__init__(document=document, degree=degree, settings=settings)

    def render(self) -> None:
        """Render a single degree."""

        log.debug("Rendering degree section.")

        _paragraph_lines = []

        if self.degree.school and self.settings.school:
            _paragraph_lines.append(f"School: {self.degree.school}")

        if self.degree.degree and self.settings.degree:
            _paragraph_lines.append(f"Degree: {self.degree.degree}")

        if self.degree.start_date and self.settings.start_date:
            _value = self.degree.start_date.strftime("%B %Y")
            _paragraph_lines.append(f"Start Date: {_value}")

        if self.degree.end_date and self.settings.end_date:
            _value = self.degree.end_date.strftime("%B %Y")
            _paragraph_lines.append(f"End Date: {_value}")

        if self.degree.major and self.settings.major:
            _paragraph_lines.append(f"Major: {self.degree.major}")

        if self.degree.gpa and self.settings.gpa:
            _paragraph_lines.append(f"GPA: {self.degree.gpa}")

        if len(_paragraph_lines) > 0:
            self.document.add_paragraph("\n".join(_paragraph_lines))


class RenderEducationSection(ResumeRenderEducationBase):
    """Render Education Section."""

    def __init__(
        self,
        document: docx.document.Document,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the basic education renderer."""
        super().__init__(document, education, settings)

    def render(self) -> None:
        """Render the education section."""

        log.debug("Rendering education section.")

        if not self.settings.degrees:
            return

        self.document.add_heading("Education", level=3)
        for _degree in self.education.degrees:
            RenderDegreeSection(
                document=self.document,
                degree=_degree,
                settings=self.settings,
            ).render()
            self.document.add_paragraph()
