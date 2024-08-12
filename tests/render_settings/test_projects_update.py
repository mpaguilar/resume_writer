from resume_writer.resume_render.render_settings import (
    ResumeProjectsSettings,
)


class TestResumeProjectsSettings:
    def setup_method(self):
        self.settings = ResumeProjectsSettings()

    def test_update_from_dict(self):
        data_dict = {"overview": False, "skills": False}
        self.settings.update_from_dict(data_dict)
        assert self.settings.overview is False
        assert self.settings.skills is False
