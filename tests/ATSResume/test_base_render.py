import pytest

from unittest.mock import Mock
from docx.document import Document
from resume_writer.docx_render.docx_render_base import (
    DocxResumeBase,
    DocxPersonalBase,
    DocxExperienceBase,
    DocxEducationBase,
    DocxCertificationsBase,
)
from models.resume import Resume
from docx_render.resume_settings import (
    ResumeSettings,
    ResumePersonalSettings,
    ResumeExperienceSettings,
    ResumeEducationSettings,
    ResumeCertificationsSettings,
)

@pytest.fixture()
def resume():
    return Mock(spec=Resume)

@pytest.fixture()
def document():
    return Mock(spec=Document)

@pytest.fixture()
def settings():
    return ResumeSettings()

@pytest.fixture()
def personal_settings():
    return ResumePersonalSettings()

@pytest.fixture()
def experience_settings():
    return ResumeExperienceSettings()

@pytest.fixture()
def education_settings():
    return ResumeEducationSettings()

@pytest.fixture()
def certifications_settings():
    return ResumeCertificationsSettings()

def test_docx_resume_base_init(resume, settings):
    renderer = DocxResumeBase(resume, settings)
    assert renderer.resume == resume
    assert renderer.settings == settings
    assert isinstance(renderer.document, Document)

def test_docx_resume_base_render(resume, settings):
    renderer = DocxResumeBase(resume, settings)
    with pytest.raises(NotImplementedError):
        renderer.render()

def test_docx_personal_base_init(document, resume, personal_settings):
    renderer = DocxPersonalBase(document, resume, personal_settings)
    assert renderer.document == document
    assert renderer.resume == resume
    assert renderer.settings == personal_settings

def test_docx_personal_base_render(document, resume, personal_settings):
    renderer = DocxPersonalBase(document, resume, personal_settings)
    with pytest.raises(NotImplementedError):
        renderer.render()

def test_docx_experience_base_init(document, resume, experience_settings):
    renderer = DocxExperienceBase(document, resume, experience_settings)
    assert renderer.document == document
    assert renderer.resume == resume
    assert renderer.settings == experience_settings

def test_docx_experience_base_render(document, resume, experience_settings):
    renderer = DocxExperienceBase(document, resume, experience_settings)
    with pytest.raises(NotImplementedError):
        renderer.render()

def test_docx_education_base_init(document, resume, education_settings):
    renderer = DocxEducationBase(document, resume, education_settings)
    assert renderer.document == document
    assert renderer.resume == resume
    assert renderer.settings == education_settings

def test_docx_education_base_render(document, resume, education_settings):
    renderer = DocxEducationBase(document, resume, education_settings)
    with pytest.raises(NotImplementedError):
        renderer.render()

def test_docx_certifications_base_init(document, resume, certifications_settings):
    renderer = DocxCertificationsBase(document, resume, certifications_settings)
    assert renderer.document == document
    assert renderer.resume == resume
    assert renderer.settings == certifications_settings

def test_docx_certifications_base_render(document, resume, certifications_settings):
    renderer = DocxCertificationsBase(document, resume, certifications_settings)
    with pytest.raises(NotImplementedError):
        renderer.render()

