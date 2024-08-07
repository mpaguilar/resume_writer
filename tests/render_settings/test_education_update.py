from resume_writer.docx_render.resume_settings import (
    ResumeEducationSettings,
)


class TestResumeSettingsBase:
    def setup_method(self):
        self.resume_settings = ResumeEducationSettings()

    def test_update_from_dict(self):
        data_dict = {"degrees": False, "experience": True}
        self.resume_settings.update_from_dict(data_dict)
        assert self.resume_settings.degrees is False


class TestResumeEducationSettings:
    def setup_method(self):
        self.education_settings = ResumeEducationSettings()

    def test_initialization(self):
        assert self.education_settings.degrees is True

    def test_update_from_dict(self):
        data_dict = {"degrees": False}
        self.education_settings.update_from_dict(data_dict)
        assert self.education_settings.degrees is False

    def test_update_from_dict_nonexistent_key(self):
        data_dict = {"nonexistent_key": "value"}
        self.education_settings.update_from_dict(data_dict)
        assert not hasattr(self.education_settings, "nonexistent_key")
