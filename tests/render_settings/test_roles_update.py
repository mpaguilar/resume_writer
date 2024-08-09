from resume_writer.docx_render.resume_settings import (
    ResumeExperienceSettings,
)


class TestResumeExperienceSettings:
    def setup_method(self):
        self.settings = ResumeExperienceSettings()

    def test_update_from_dict(self):
        data_dict = {"summary": False, "skills": False}
        self.settings.update_from_dict(data_dict)
        assert self.settings.summary is False
        assert self.settings.skills is False
