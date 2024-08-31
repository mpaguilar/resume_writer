import logging

import docx.document

from resume_writer.models.resume import Resume
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.resume_render_base import ResumeRenderBase
from resume_writer.resume_render.simple.simple_certifications_section import (
    BasicRenderCertificationsSection,
)
from resume_writer.resume_render.simple.simple_education_section import (
    BasicRenderEducationSection,
)
from resume_writer.resume_render.simple.simple_experience_section import (
    BasicRenderExperienceSection,
)
from resume_writer.resume_render.simple.simple_personal_section import (
    BasicRenderPersonalSection,
)

log = logging.getLogger(__name__)


class BasicRenderResume(ResumeRenderBase):
    """Render a resume in basic format."""

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeRenderSettings,
    ):
        """Initialize basic resume renderer."""
        super().__init__(document, resume, settings)

    def render(self) -> None:
        """Render the resume by adding different sections based on settings.

        Parameters
        ----------
        self : object
            The instance of the class containing resume and settings.

        Steps
        -----
        1. Render personal section if personal data exists and settings allow.
        2. Render certifications section if certifications data exists
        and settings allow.
        3. Render education section if education data exists and settings allow.
        4. Render experience section if experience data exists and settings allow.

        Returns
        -------
        None

        """

        if self.resume.personal and self.settings.personal:
            BasicRenderPersonalSection(
                self.document,
                self.resume.personal,
                self.settings.personal_settings,
            ).render()

        if self.resume.certifications and self.settings.certifications:
            BasicRenderCertificationsSection(
                self.document,
                self.resume.certifications,
                self.settings.certifications_settings,
            ).render()

        if self.resume.education and self.settings.education:
            BasicRenderEducationSection(
                self.document,
                self.resume.education,
                self.settings.education_settings,
            ).render()

        if self.resume.experience and self.settings.experience:
            BasicRenderExperienceSection(
                self.document,
                self.resume.experience,
                self.settings.experience_settings,
            ).render()
