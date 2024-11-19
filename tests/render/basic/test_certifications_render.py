import pytest
from datetime import datetime

from unittest.mock import Mock, MagicMock
import docx.document

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.models.parsers import ParseContext


from resume_writer.resume_render.render_settings import (
    ResumeCertificationsSettings,
)

from resume_writer.resume_render.basic.certifications_section import (
    RenderCertificationsSection,
)


@pytest.fixture
def document():
    _doc = Mock(spec=docx.document.Document)
    _doc.styles = MagicMock()
    _doc.styles["Normal"] = MagicMock()
    _doc.sections = MagicMock()
    _doc.sections[0] = MagicMock()

    return _doc


@pytest.fixture
def settings():
    return ResumeCertificationsSettings()

@pytest.fixture
def context():
    return Mock(spec=ParseContext)


@pytest.fixture
def certifications(context):
    _certification = Mock(spec=Certification)
    _certification.name = "Certification Name"
    _certification.issuer = "Certification Issuer"
    _certification.issued = datetime(2020, 1, 1)
    _certification.expires = datetime(2025, 1, 1)

    _certifications = Certifications([_certification], parse_context=context)

    return _certifications


def test_render_certifications_section(document, settings, certifications):
    section = RenderCertificationsSection(
        document=document,
        certifications=certifications,
        settings=settings,
    )

    section.render()
