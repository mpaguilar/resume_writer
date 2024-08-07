from resume_writer.docx_render.resume_settings import (
    ResumeRolesSettings,
)


class TestResumeRolesSettings:
    def setup_method(self):
        self.settings = ResumeRolesSettings()

    def test_initialization(self):
        assert self.settings.summary is True
        assert self.settings.skills is True
        assert self.settings.responsibilities is True
        assert self.settings.accomplishments is True
        assert self.settings.reason_for_leaving is True
        assert self.settings.location is True
        assert self.settings.job_category is True
        assert self.settings.employment_type is True
        assert self.settings.agency_name is True

    def test_update_from_dict(self):
        data_dict = {"summary": False, "skills": False}
        self.settings.update_from_dict(data_dict)
        assert self.settings.summary is False
        assert self.settings.skills is False
