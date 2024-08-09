import logging

from docx_render.ats_certifications_section import ATSCertificationsSection
from docx_render.ats_education_section import ATSEducationSection
from docx_render.ats_experience_section import ATSExperienceSection
from docx_render.ats_personal_section import ATSPersonalSection
from docx_render.docx_render_base import DocxResumeBase
from docx_render.resume_settings import ResumeSettings
from models.resume import Resume

log = logging.getLogger(__name__)


class ATSResume(DocxResumeBase):
    """Represent and render an ATS-friendly Word resume."""

    def __init__(self, resume: Resume, settings: ResumeSettings | None):
        """Initialize a blank ATS-friendly Word document."""

        super().__init__(resume=resume, settings=settings)

    def render(self) -> None:
        """Render an ATS-friendly Word document."""

        log.info("Rendering ATS friendly Word document")

        if self.settings.personal:
            ATSPersonalSection(
                document=self.document,
                resume=self.resume,
                settings=self.settings.personal_settings,
            ).render()

        if self.settings.education:
            ATSEducationSection(
                document=self.document,
                resume=self.resume,
                settings=self.settings.education_settings,
            ).render()

        if self.settings.certifications:
            ATSCertificationsSection(
                document=self.document,
                resume=self.resume,
                settings=self.settings.certifications_settings,
            ).render()

        if self.settings.roles:
            ATSExperienceSection(
                document=self.document,
                resume=self.resume,
                settings=self.settings.roles_settings,
            ).render()
