import pytest
from datetime import datetime

from unittest.mock import Mock
import docx.document

from resume_writer.models.certifications import Certification, Certifications


from resume_writer.resume_render.render_settings import (
    ResumeCertificationsSettings,
)

from resume_writer.resume_render.basic.basic_certifications_section import (
    BasicRenderCertificationsSection,
)


@pytest.fixture()
def document():
    return Mock(spec=docx.document.Document)


@pytest.fixture()
def settings():
    return ResumeCertificationsSettings()


@pytest.fixture()
def certifications():
    _certification = Mock(spec=Certification)
    _certification.name = "Certification Name"
    _certification.issuer = "Certification Issuer"
    _certification.issued = datetime(2020, 1, 1)
    _certification.expires = datetime(2025, 1, 1)

    _certifications = Certifications([_certification])

    return _certifications


def test_render_certifications_section(document, settings, certifications):
    section = BasicRenderCertificationsSection(
        document=document,
        certifications=certifications,
        settings=settings,
    )

    section.render()
