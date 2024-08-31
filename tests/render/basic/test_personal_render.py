import pytest

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.resume_render.basic.basic_personal_section import (
    BasicRenderPersonalSection,
)

from resume_writer.models.personal import (
    Personal,
    ContactInfo,
    Banner,
    VisaStatus,
    Websites,
    Note,
)

from resume_writer.resume_render.render_settings import ResumePersonalSettings


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()

    return _doc


@pytest.fixture
def contact_info():
    _contact_info = Mock(spec=ContactInfo)
    _contact_info.name = "John Doe"
    _contact_info.email = "test"
    _contact_info.phone = "test"
    _contact_info.location = "test"

    return _contact_info


@pytest.fixture
def banner():
    _banner = Mock(spec=Banner)
    _banner.text = "test"
    return _banner


@pytest.fixture
def visa_status():
    _visa_status = Mock(spec=VisaStatus)
    _visa_status.work_authorization = "test"
    _visa_status.require_sponsorship = True
    return _visa_status


@pytest.fixture
def websites():
    _websites = Mock(spec=Websites)
    _websites.github = "github"
    _websites.linkedin = "linkedin"
    _websites.website = "website"
    _websites.twitter = "twitter"

    return _websites


@pytest.fixture
def note():
    _note = Mock(spec=Note)
    _note.text = "test"
    return _note


@pytest.fixture
def personal(contact_info, banner, visa_status, websites, note):
    _personal = Mock(spec=Personal)
    _personal.contact_info = contact_info
    _personal.banner = banner
    _personal.visa_status = visa_status
    _personal.websites = websites
    _personal.note = note

    return _personal


@pytest.fixture
def settings():
    return ResumePersonalSettings()


def test_render_personal_section(document, personal, settings):
    section = BasicRenderPersonalSection(
        document=document,
        personal=personal,
        settings=settings,
    )
    section.render()
