import pytest
from resume_writer.docx_render.resume_settings import (
    ResumeSettingsBase,
    ResumeCertificationsSettings,
)


@pytest.fixture()
def resume_settings_base():
    return ResumeSettingsBase()


@pytest.fixture()
def resume_certifications_settings():
    return ResumeCertificationsSettings()


def test_update_from_dict_with_nonexistent_key(resume_settings_base):
    data_dict = {"nonexistent_key": "test_value"}
    resume_settings_base.update_from_dict(data_dict)
    assert not hasattr(resume_settings_base, "nonexistent_key")


def test_resume_certifications_settings_initialization(resume_certifications_settings):
    assert resume_certifications_settings.include_expires is True


def test_resume_certifications_settings_update_from_dict(
    resume_certifications_settings,
):
    data_dict = {"include_expires": False}
    resume_certifications_settings.update_from_dict(data_dict)
    assert resume_certifications_settings.include_expires is False
