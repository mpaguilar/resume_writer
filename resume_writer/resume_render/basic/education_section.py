import logging

import docx.document
from docx.shared import Pt
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

        _paragraph = self.document.add_paragraph()

        if self.degree.school and self.settings.school:
            _school_run = _paragraph.add_run(f"{self.degree.school}")
            _school_run.bold = True
            _school_run.underline = True
            _school_run.font.size = Pt(self.font_size + 2)
            _school_run.add_break()

        if self.degree.degree and self.settings.degree:
            _degree_run = _paragraph.add_run(f"{self.degree.degree}")
            _degree_run.bold = True
            _degree_run.add_break()

        if self.degree.start_date and self.settings.start_date:
            _value = self.degree.start_date.strftime("%B %Y")
            _start_date_run = _paragraph.add_run(f"{_value}")
            if self.settings.end_date:
                _paragraph.add_run(" - ")
            else:
                _start_date_run.add_break()

        if self.degree.end_date and self.settings.end_date:
            if self.degree.end_date is None:
                _value = "Present"
            else:
                _value = self.degree.end_date.strftime("%B %Y")
            _end_date_run = _paragraph.add_run(f"{_value}")
            _end_date_run.add_break()

        if self.degree.major and self.settings.major:
            _degree_run = _paragraph.add_run(f"{self.degree.major}")
            _degree_run.add_break()

        if self.degree.gpa and self.settings.gpa:
            _gpa_run = _paragraph.add_run(f"GPA: {self.degree.gpa}")
            _gpa_run.add_break()



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
