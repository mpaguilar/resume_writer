import logging

from jinja2 import Environment
from resume_render.resume_render_text_base import (
    ResumeRenderBase,
)
from utils.html_doc import HtmlDoc

from resume_writer.models.resume import Resume
from resume_writer.resume_render.html.certifications_section import (
    RenderCertificationsSection,
)
from resume_writer.resume_render.html.education_section import (
    RenderEducationSection,
)
from resume_writer.resume_render.html.executive_summary_section import (
    RenderExecutiveSummarySection,
)
from resume_writer.resume_render.html.experience_section import (
    RenderExperienceSection,
)
from resume_writer.resume_render.html.personal_section import (
    RenderPersonalSection,
)
from resume_writer.resume_render.html.skills_matrix_section import (
    RenderSkillsMatrixSection,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings

log = logging.getLogger(__name__)

class RenderResume(ResumeRenderBase):
    """Render a resume in basic format."""

    def __init__(
        self,
        document: HtmlDoc,
        jinja_env: Environment,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize basic resume renderer."""
        super().__init__(
            document=document,
            jinja_env=jinja_env,
            resume=resume,
            settings=settings,
        )

    def render(self) -> None:
        """Render the resume."""

        if self.resume.personal and self.settings.personal:
            RenderPersonalSection(
                document=self.document,
                personal=self.resume.personal,
                jinja_env=self.jinja_env,
                settings=self.settings.personal_settings,
            ).render()

        if self.resume.education and self.settings.education:
            RenderEducationSection(
                document=self.document,
                jinja_env=self.jinja_env,
                education=self.resume.education,
                settings=self.settings.education_settings,
            ).render()
"""
        if self.resume.certifications and self.settings.certifications:
            RenderCertificationsSection(
                self.document,
                self.resume.certifications,
                self.settings.certifications_settings,
            ).render()

        # the executive summary is built from experience, so it has to exist
        if self.resume.experience and self.settings.executive_summary:
            self.document.add_heading("Executive Summary", 2)

            RenderExecutiveSummarySection(
                self.document,
                self.resume.experience,
                self.settings.executive_summary_settings,
            ).render()

        # the skills section is built from experience, so it has to exist
        if self.resume.experience and self.settings.skills_matrix:
            RenderSkillsMatrixSection(
                self.document,
                self.resume.experience,
                self.settings.skills_matrix_settings,
            ).render()

        # render all the roles
        if self.resume.experience and self.settings.experience:
            RenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
"""
