import logging

import docx.document

from resume_writer.models.experience import (
    Experience,
)
from resume_writer.resume_render.render_settings import (
    ResumeExecutiveSummarySettings,
)
from resume_writer.resume_render.resume_render_base import (
    ResumeRenderExecutiveSummaryBase,
)

log = logging.getLogger(__name__)


class RenderExecutiveSummarySection(ResumeRenderExecutiveSummaryBase):
    """Render experience for a functional resume."""

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeExecutiveSummarySettings,
    ) -> None:
        """Initialize experience render object."""
        log.debug("Initializing functional experience render object.")
        super().__init__(document=document, experience=experience, settings=settings)

    def render(self) -> None:
        """Render experience section for functional resume."""

        log.debug("Rendering functional experience section.")

        if not self.experience.roles:
            raise ValueError("Experience must have roles for a functional resume.")

        # collect all job categories
        _roles = self.experience.roles
        _job_categories = set()

        # collect roles for each job category
        for _role in _roles:
            if _role.basics.job_category:
                _job_categories.add(_role.basics.job_category)

        # render each job category with roles

        for _category in self.settings.categories:
            _category_roles = [
                _role for _role in _roles if _role.basics.job_category == _category
            ]
            self.document.add_heading(_category, level=4)

            for _role in _category_roles:
                _paragraph = self.document.add_paragraph()

                _paragraph.style = "List Bullet"
                _paragraph.add_run(f"{_role.summary.summary}")
                _run = _paragraph.add_run(f" ({_role.basics.company})")
                _run.italic = True
