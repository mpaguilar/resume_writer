import logging

import docx.document
from resume_render.render_settings import ResumeEducationSettings
from resume_render.resume_render_base import (
    ResumeRenderDegreeBase,
    ResumeRenderEducationBase,
)

from resume_writer.models.education import Degree, Education

log = logging.getLogger(__name__)


class BasicRenderDegreeSection(ResumeRenderDegreeBase):
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

        _education_paragraph = self.document.add_paragraph()
        _education_run = _education_paragraph.add_run()

        _education_text = ""

        # first line
        if self.degree.school and self.settings.school:
            _education_text += f"{self.degree.school}"

        if self.degree.start_date and self.settings.start_date:
            _value = self.degree.start_date.strftime("%B %Y")
            if _education_text:
                _education_text += f" ({_value}"

        if self.degree.end_date and self.settings.end_date:
            _value = self.degree.end_date.strftime("%B %Y")
            if _education_text:
                _education_text += f" - {_value})"
            else:
                _education_text += f"({_value})"
        elif self.settings.end_date:
            if _education_text:
                _education_text += " - Present)"
            else:
                _education_text += "(Current)"

        _education_run.add_text(_education_text)
        _education_run.font.bold = True

        # second line

        _second_line = "\r" # TODO: why does '\r' work, and '\n' doesn't?

        if self.degree.degree and self.settings.degree:
            _second_line += f"Degree: {self.degree.degree}"

        if self.degree.major and self.settings.major:
            _second_line += f", Major: {self.degree.major}"

        if self.degree.gpa and self.settings.gpa:
            _second_line += f", GPA: {self.degree.gpa}"

        if _second_line != "\r":
            _second_line_run = _education_paragraph.add_run()
            _second_line_run.add_text(_second_line)


class BasicRenderEducationSection(ResumeRenderEducationBase):
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

        self.document.add_heading("Education", level=2)
        for _degree in self.education.degrees:
            BasicRenderDegreeSection(
                document=self.document,
                degree=_degree,
                settings=self.settings,
            ).render()
