import logging

import docx.document

from resume_writer.models.resume import Resume
from resume_writer.resume_render.functional.certifications_section import (
    BasicRenderCertificationsSection,
)
from resume_writer.resume_render.functional.education_section import (
    BasicRenderEducationSection,
)
from resume_writer.resume_render.functional.experience_section import (
    BasicRenderExperienceSection,
)
from resume_writer.resume_render.functional.personal_section import (
    BasicRenderPersonalSection,
)
from resume_writer.resume_render.render_settings import ResumeSettings
from resume_writer.resume_render.resume_render_base import ResumeRenderBase

log = logging.getLogger(__name__)


class BasicRenderResume(ResumeRenderBase):
    """Render a resume in basic format."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeSettings,
    ):
        """Initialize basic resume renderer."""
        super().__init__(document, resume, settings)

    def render(self) -> None:
        """Render the resume."""

        if self.resume.personal and self.settings.personal:
            BasicRenderPersonalSection(
                self.document,
                self.resume.personal,
                self.settings.personal_settings,
            ).render()

        if self.resume.education and self.settings.education:
            BasicRenderEducationSection(
                self.document,
                self.resume.education,
                self.settings.education_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            BasicRenderCertificationsSection(
                self.document,
                self.resume.certifications,
                self.settings.certifications_settings,
            ).render()

        if self.resume.experience and self.settings.experience:
            BasicRenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
