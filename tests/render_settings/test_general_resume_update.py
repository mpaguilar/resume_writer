import pytest

from resume_writer.resume_render.render_settings import (
    ResumeCertificationsSettings,
    ResumeEducationSettings,
    ResumeExperienceSettings,
    ResumeProjectsSettings,
    ResumeRolesSettings,
    ResumePersonalSettings,
    ResumeSettings,
)


@pytest.fixture
def test_dict():
    _settings_dict = {
        "resume": {
            "render": {
                "personal": False,
                "education": False,
                "certifications": False,
                "experience": False,
                "font_size": 20,
                "margin_width": 100,
                "executive_summary": False,
                "skills_matrix": False,

                "section": {
                    "personal": {
                        "contact_info": False,
                        "banner": False,
                        "visa_status": False,
                        "websites": False,
                        "note": False,
                        "name": False,
                        "email": False,
                        "phone": False,
                        "location": False,
                        "linkedin": False,
                        "github": False,
                        "website": False,
                        "twitter": False,
                        "require_sponsorship": False,
                        "work_authorization": False,
                    },
                    "experience": {
                        "roles": False,
                        "projects": False,
                        "section": {
                            "projects": {
                                "overview": False,
                                "description": False,
                                "skills": False,
                                "title": False,
                                "url": False,
                                "url_description": False,
                                "start_date": False,
                                "end_date": False,
                            },
                            "roles": {
                                "summary": False,
                                "skills": False,
                                "responsibilities": False,
                                "reason_for_change": False,
                                "location": False,
                                "job_category": False,
                                "employment_type": False,
                                "agency_name": False,
                                "start_date": False,
                                "end_date": False,
                            },
                            "executive_summary": {
                                "categories": "Category1\nCategory2",
                                "skills": "Skill1\nSkill2",
                            },
                        },
                    },
                    "certifications": {
                        "name": False,
                        "issuer": False,
                        "issued": False,
                        "expires": False,
                    },
                    "education": {
                        "degrees": False,
                        "school": False,
                        "degree": False,
                        "start_date": False,
                        "end_date": False,
                        "gpa": False,
                        "major": False,
                    },
                },
            },
        },
    }

    return _settings_dict


def test_resume_settings(test_dict):
    _resume_settings = ResumeSettings()
    _resume_settings.update_from_dict(test_dict["resume"]["render"])
    assert _resume_settings.personal is False
    assert _resume_settings.education is False
    assert _resume_settings.certifications is False
    assert _resume_settings.experience is False
    assert _resume_settings.font_size == 20
    assert _resume_settings.margin_width == 100
    assert _resume_settings.executive_summary is False

    # test the subsections
    _personal = _resume_settings.personal_settings
    assert _personal.contact_info is False
    assert _personal.banner is False
    assert _personal.visa_status is False
    assert _personal.websites is False
    assert _personal.note is False

    _education = _resume_settings.education_settings
    assert _education.degrees is False
    assert _education.school is False
    assert _education.degree is False
    assert _education.start_date is False
    assert _education.end_date is False
    assert _education.gpa is False
    assert _education.major is False

    _certifications = _resume_settings.certifications_settings
    assert _certifications.name is False
    assert _certifications.issuer is False
    assert _certifications.issued is False
    assert _certifications.expires is False

    _experience = _resume_settings.experience_settings
    assert _experience.roles is False
    assert _experience.projects is False


def test_personal_settings(test_dict):
    _personal_settings = ResumePersonalSettings()
    _personal_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["personal"],
    )
    assert _personal_settings.contact_info is False
    assert _personal_settings.banner is False
    assert _personal_settings.visa_status is False
    assert _personal_settings.websites is False
    assert _personal_settings.note is False

    assert _personal_settings.name is False
    assert _personal_settings.email is False
    assert _personal_settings.phone is False
    assert _personal_settings.location is False

    assert _personal_settings.linkedin is False
    assert _personal_settings.github is False
    assert _personal_settings.website is False
    assert _personal_settings.twitter is False

    assert _personal_settings.require_sponsorship is False
    assert _personal_settings.work_authorization is False


def test_education_settings(test_dict):
    _education_settings = ResumeEducationSettings()
    _education_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["education"],
    )
    assert _education_settings.degrees is False

    assert _education_settings.school is False
    assert _education_settings.degree is False
    assert _education_settings.start_date is False
    assert _education_settings.end_date is False
    assert _education_settings.gpa is False
    assert _education_settings.major is False


def test_certifications_settings(test_dict):
    _certifications_settings = ResumeCertificationsSettings()
    _certifications_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["certifications"],
    )
    assert _certifications_settings.name is False
    assert _certifications_settings.issuer is False
    assert _certifications_settings.issued is False
    assert _certifications_settings.expires is False


def test_projects_settings(test_dict):
    _projects_settings = ResumeProjectsSettings()
    _projects_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["experience"]["section"]["projects"],
    )
    assert _projects_settings.overview is False
    assert _projects_settings.description is False
    assert _projects_settings.skills is False

    assert _projects_settings.title is False
    assert _projects_settings.url is False
    assert _projects_settings.url_description is False
    assert _projects_settings.start_date is False
    assert _projects_settings.end_date is False


def test_roles_settings(test_dict):
    _roles_settings = ResumeRolesSettings()
    _roles_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["experience"]["section"]["roles"],
    )

    assert _roles_settings.summary is False
    assert _roles_settings.skills is False
    assert _roles_settings.responsibilities is False
    assert _roles_settings.reason_for_change is False
    assert _roles_settings.location is False
    assert _roles_settings.job_category is False
    assert _roles_settings.employment_type is False
    assert _roles_settings.agency_name is False
    assert _roles_settings.start_date is False
    assert _roles_settings.end_date is False


def test_experience_settings(test_dict):
    _experience_settings = ResumeExperienceSettings()
    _experience_settings.update_from_dict(
        test_dict["resume"]["render"]["section"]["experience"],
    )
    assert _experience_settings.roles is False
    assert _experience_settings.projects is False

    # check subsections

    _project_settings = _experience_settings.projects_settings
    assert _project_settings.overview is False
    assert _project_settings.description is False
    assert _project_settings.skills is False

    _role_settings = _experience_settings.roles_settings
    assert _role_settings.summary is False
    assert _role_settings.skills is False

    _executive_summary_settings = _experience_settings.executive_summary_settings
    assert _executive_summary_settings.categories == ["Category1", "Category2"]
    assert _executive_summary_settings.skills == ["Skill1", "Skill2"]
