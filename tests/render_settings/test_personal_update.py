import pytest
from resume_writer.docx_render.resume_settings import ResumePersonalSettings


@pytest.fixture()
def resume_settings():
    return ResumePersonalSettings()


def test_initialization(resume_settings):
    assert resume_settings.contact_info is True
    assert resume_settings.banner is True
    assert resume_settings.visa_status is True
    assert resume_settings.websites is True
    assert resume_settings.note is True


def test_update_from_dict(resume_settings):
    data_dict = {
        "contact_info": False,
        "banner": False,
        "visa_status": False,
        "websites": False,
        "note": False,
    }
    resume_settings.update_from_dict(data_dict)
    assert resume_settings.contact_info is False
    assert resume_settings.banner is False
    assert resume_settings.visa_status is False
    assert resume_settings.websites is False
    assert resume_settings.note is False


def test_update_from_dict_with_invalid_key(resume_settings):
    data_dict = {"invalid_key": False}
    resume_settings.update_from_dict(data_dict)
    assert not hasattr(resume_settings, "invalid_key")


def test_update_from_dict_with_empty_dict(resume_settings):
    data_dict = {}
    resume_settings.update_from_dict(data_dict)
    assert resume_settings.contact_info is True
    assert resume_settings.banner is True
    assert resume_settings.visa_status is True
    assert resume_settings.websites is True
    assert resume_settings.note is True
