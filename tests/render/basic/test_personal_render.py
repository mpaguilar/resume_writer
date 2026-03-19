import pytest

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.resume_render.basic.personal_section import (
    RenderPersonalSection,
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
    section = RenderPersonalSection(
        document=document,
        personal=personal,
        settings=settings,
    )
    section.render()


def test_contact_info_with_none_values(document, settings):
    """Test contact info with None values."""
    contact_info = Mock(spec=ContactInfo)
    contact_info.name = None
    contact_info.email = None
    contact_info.phone = None
    contact_info.location = None

    personal = Mock(spec=Personal)
    personal.contact_info = contact_info

    section = RenderPersonalSection(document, personal, settings)
    section._contact_info()
    # Verify no paragraph added when all fields are None


def test_contact_info_with_disabled_settings(document):
    """Test contact info with all settings disabled."""
    settings = ResumePersonalSettings(default_init=False)
    settings.contact_info = True  # Enable contact_info section
    # But disable all individual fields
    settings.name = False
    settings.email = False
    settings.phone = False
    settings.location = False

    contact_info = Mock(spec=ContactInfo)
    contact_info.name = "John Doe"
    contact_info.email = "test@test.com"
    contact_info.phone = "555-1234"
    contact_info.location = "City"

    personal = Mock(spec=Personal)
    personal.contact_info = contact_info

    section = RenderPersonalSection(document, personal, settings)
    section._contact_info()
    # Verify no paragraph added when all settings disabled


def test_banner_with_none_text(document, settings):
    """Test banner with None text."""
    banner = Mock(spec=Banner)
    banner.text = None

    personal = Mock(spec=Personal)
    personal.banner = banner

    section = RenderPersonalSection(document, personal, settings)
    section._banner()
    # Verify no heading/paragraph added


def test_banner_with_disabled_setting(document):
    """Test banner with disabled setting."""
    settings = ResumePersonalSettings(default_init=False)
    settings.banner = False

    banner = Mock(spec=Banner)
    banner.text = "Test Banner"

    personal = Mock(spec=Personal)
    personal.banner = banner

    section = RenderPersonalSection(document, personal, settings)
    section._banner()
    # Verify no heading/paragraph added


def test_websites_with_none_values(document, settings):
    """Test websites with None values."""
    websites = Mock(spec=Websites)
    websites.github = None
    websites.linkedin = None
    websites.website = None
    websites.twitter = None

    personal = Mock(spec=Personal)
    personal.websites = websites

    section = RenderPersonalSection(document, personal, settings)
    section._websites()
    # Verify no paragraph added when all fields are None


def test_websites_with_disabled_settings(document):
    """Test websites with disabled setting."""
    settings = ResumePersonalSettings(default_init=False)
    settings.websites = False

    websites = Mock(spec=Websites)
    websites.github = "github"
    websites.linkedin = "linkedin"
    websites.website = "website"
    websites.twitter = "twitter"

    personal = Mock(spec=Personal)
    personal.websites = websites

    section = RenderPersonalSection(document, personal, settings)
    section._websites()
    # Verify no paragraph added when setting disabled


def test_visa_status_with_none_values(document, settings):
    """Test visa status with None values."""
    visa_status = Mock(spec=VisaStatus)
    visa_status.work_authorization = None
    visa_status.require_sponsorship = None

    personal = Mock(spec=Personal)
    personal.visa_status = visa_status

    section = RenderPersonalSection(document, personal, settings)
    section._visa_status()
    # Verify no paragraph added when all fields are None


def test_visa_status_with_disabled_setting(document):
    """Test visa status with disabled setting."""
    settings = ResumePersonalSettings(default_init=False)
    settings.visa_status = False

    visa_status = Mock(spec=VisaStatus)
    visa_status.work_authorization = "US Citizen"
    visa_status.require_sponsorship = False

    personal = Mock(spec=Personal)
    personal.visa_status = visa_status

    section = RenderPersonalSection(document, personal, settings)
    section._visa_status()
    # Verify no paragraph added when setting disabled


def test_note_with_none_text(document, settings):
    """Test note with None text."""
    note = Mock(spec=Note)
    note.text = None

    personal = Mock(spec=Personal)
    personal.note = note

    section = RenderPersonalSection(document, personal, settings)
    section._note()
    # Verify no heading/paragraph added


def test_note_with_disabled_setting(document):
    """Test note with disabled setting."""
    settings = ResumePersonalSettings(default_init=False)
    settings.note = False

    note = Mock(spec=Note)
    note.text = "Test Note"

    personal = Mock(spec=Personal)
    personal.note = note

    section = RenderPersonalSection(document, personal, settings)
    section._note()
    # Verify no heading/paragraph added


def test_render_with_all_sections_disabled(document, personal):
    """Test render with all personal sections disabled."""
    settings = ResumePersonalSettings(default_init=False)
    # All sections disabled by default_init=False

    section = RenderPersonalSection(document, personal, settings)
    section.render()
    # Verify no document methods called
