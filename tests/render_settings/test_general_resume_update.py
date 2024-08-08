import pytest
from resume_writer.docx_render.resume_settings import ResumeSettingsBase, ResumeSettings


@pytest.fixture()
def base_settings():
    return ResumeSettingsBase()


@pytest.fixture()
def resume_settings():
    return ResumeSettings()


def test_update_from_dict_existing_key(base_settings):
    data_dict = {"existing_key": "new_value"}
    setattr(base_settings, "existing_key", "old_value")
    base_settings.update_from_dict(data_dict)
    assert base_settings.existing_key == "new_value"


def test_update_from_dict_non_existing_key(base_settings):
    data_dict = {"non_existing_key": "new_value"}
    base_settings.update_from_dict(data_dict)
    assert not hasattr(base_settings, "non_existing_key")


def test_resume_settings_initialization(resume_settings):
    assert hasattr(resume_settings, "personal")
    assert hasattr(resume_settings, "education")
    assert hasattr(resume_settings, "certifications")
    assert hasattr(resume_settings, "roles")


def test_resume_settings_update_from_dict(resume_settings):
    data_dict = {"personal": False, "education": False}
    resume_settings.update_from_dict(data_dict)
    assert resume_settings.personal is False
    assert resume_settings.education is False
