class ResumeSettingsBase:
    """Base class for resume settings."""

    def update_from_dict(self, data_dict : dict | None = None) -> None:
        """Update the settings from a dictionary."""

        if data_dict is None:
            return

        for key, value in data_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ResumePersonalSettings(ResumeSettingsBase):
    """Control what parts of a resume's personal section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.contact_info = True
        self.banner = True
        self.visa_status = True
        self.websites = True
        self.note = True


class ResumeEducationSettings(ResumeSettingsBase):
    """Control what parts of a resume's education section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.degrees = True
        self.gpa = True
        self.major = True


class ResumeCertificationsSettings(ResumeSettingsBase):
    """Control what parts of a resume's certifications section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.include_expires = True


class ResumeExperienceSettings(ResumeSettingsBase):
    """Control what parts of a resume's roles section are rendered."""

    def __init__(self) -> None:
        """Initialize everything to True."""

        # title is required
        self.summary = True
        self.skills = True
        self.responsibilities = True
        # basics
        self.accomplishments = True
        self.reason_for_leaving = True
        self.location = True
        self.job_category = True
        self.employment_type = True
        self.agency_name = True
        self.start_date = True
        self.end_date = True


class ResumeSettings(ResumeSettingsBase):
    """Control what parts of a resume are rendered."""

    def __init__(self):
        """Initialize all settings with appropriate objects."""

        self.personal_settings = ResumePersonalSettings()
        self.personal = True

        self.education_settings = ResumeEducationSettings()
        self.education = True

        self.certifications_settings = ResumeCertificationsSettings()
        self.certifications = True

        self.roles_settings = ResumeExperienceSettings()
        self.roles = True
