class ResumeSettingsBase:
    """Base class for resume settings."""

    def update_from_dict(self, data_dict : dict) -> None:
        """Update the settings from a dictionary."""
        for key, value in data_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ResumePersonalSettings:
    """Control what parts of a resume's personal section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.contact_info = True
        self.banner = True
        self.visa_status = True
        self.websites = True
        self.note = True


class ResumeEducationSettings:
    """Control what parts of a resume's education section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.degrees = True


class ResumeCertificationsSettings:
    """Control what parts of a resume's certifications section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.include_expires = True


class ResumeRolesSettings:
    """Control what parts of a resume's roles section are rendered."""

    def __init__(self) -> None:
        """Initialize everything to True."""

        self.summary = True
        self.skills = True
        self.responsibilities = True
        self.accomplishments = True
        self.reason_for_leaving = True
        self.location = True
        self.job_category = True
        self.employment_type = True
        self.agency_name = True


class ResumeSettings(ResumeSettingsBase):
    """Control what parts of a resume are rendered."""

    def __init__(self):
        """Initialize all settings with appropriate objects."""

        self.personal = ResumePersonalSettings()
        self.render_personal = True

        self.education = ResumeEducationSettings()
        self.render_education = True

        self.certifications = ResumeCertificationsSettings()
        self.render_certifications = True

        self.roles = ResumeRolesSettings()
        self.render_roles = True
