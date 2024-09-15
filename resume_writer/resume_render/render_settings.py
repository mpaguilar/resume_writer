class ResumeSettingsBase:
    """Base class for resume settings."""

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update the settings from a dictionary."""

        if data_dict is None:
            return

        for key, value in data_dict.items():
            if key == "section":
                continue
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

        # contact info
        self.name = True
        self.email = True
        self.phone = True
        self.location = True

        # websites
        self.linkedin = True
        self.github = True
        self.website = True
        self.twitter = True

        # visa status
        self.require_sponsorship = True
        self.work_authorization = True


class ResumeEducationSettings(ResumeSettingsBase):
    """Control what parts of a resume's education section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.degrees = True  # render all degrees

        self.school = True
        self.degree = True  # render degree name
        self.start_date = True
        self.end_date = True
        self.gpa = True
        self.major = True


class ResumeCertificationsSettings(ResumeSettingsBase):
    """Control what parts of a resume's certifications section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.name = True
        self.issuer = True
        self.issued = True
        self.expires = True


class ResumeProjectsSettings(ResumeSettingsBase):
    """Control what parts of a resume's projects section are rendered."""

    def __init__(self):
        """Initialize everything to True."""

        self.overview = True
        self.description = True
        self.skills = True

        self.title = True
        self.url = True
        self.url_description = True
        self.start_date = True
        self.end_date = True


class ResumeRolesSettings(ResumeSettingsBase):
    """Control what parts of a resume's roles section are rendered."""

    def __init__(self) -> None:
        """Initialize everything to True."""

        # title is required
        self.summary = True
        self.skills = True
        self.responsibilities = True
        # basics

        self.reason_for_change = True
        self.location = True
        self.job_category = True
        self.employment_type = True
        self.agency_name = True
        self.start_date = True
        self.end_date = True


class ResumeExperienceSettings(ResumeSettingsBase):
    """Control what parts of a resume's experience section are rendered."""

    def __init__(self) -> None:
        """Initialize everything to True."""

        self.roles = True
        self.roles_settings = ResumeRolesSettings()
        self.projects = True
        self.projects_settings = ResumeProjectsSettings()
        self.executive_summary = True
        self.executive_summary_settings = ResumeExecutiveSummarySettings()
        self.skills_matrix = True
        self.skills_matrix_settings = ResumeSkillsMatrixSettings()

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update settings for experience and subsections."""
        super().update_from_dict(data_dict)
        _section = data_dict.get("section")
        if _section is None:
            return
        if "projects" in _section:
            self.projects_settings.update_from_dict(_section["projects"])
        if "roles" in _section:
            self.roles_settings.update_from_dict(_section["roles"])
        if "executive_summary" in _section:
            self.executive_summary_settings.update_from_dict(
                _section["executive_summary"],
            )
        if "skills_matrix" in _section:
            self.skills_matrix_settings.update_from_dict(_section["skills_matrix"])


class ResumeExecutiveSummarySettings(ResumeSettingsBase):
    """Control what parts of a resume's executive summary section are rendered."""

    def __init__(self) -> None:
        """Initialize everything to True."""
        self.categories: list[str] = ""

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Control what categories are rendered."""
        # categories and skills are kept as a single string, so we need to split them
        super().update_from_dict(data_dict)
        if self.categories:
            self.categories = self.categories.split("\n")


class ResumeSkillsMatrixSettings(ResumeSettingsBase):
    """Control what parts of a resume's skills matrix section are rendered."""

    def __init__(self) -> None:
        """Initialize everything.

        Set all_skills to False, because we don't usually want that.
        """

        self.skills: list[str] = ""
        self.all_skills: bool = False

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Control what skills are rendered."""
        # categories and skills are kept as a single string, so we need to split them
        super().update_from_dict(data_dict)
        if self.skills:
            self.skills = self.skills.split("\n")


class ResumeRenderSettings(ResumeSettingsBase):
    """Control what parts of a resume are rendered."""

    def __init__(self):
        """Initialize all settings with appropriate objects."""

        self.personal_settings = ResumePersonalSettings()
        self.personal = True

        self.education_settings = ResumeEducationSettings()
        self.education = True

        self.certifications_settings = ResumeCertificationsSettings()
        self.certifications = True

        self.experience_settings = ResumeExperienceSettings()
        self.experience = True

        self.skills_matrix = True
        self.skills_matrix_settings = ResumeSkillsMatrixSettings()

        self.executive_summary = True
        self.executive_summary_settings = ResumeExecutiveSummarySettings()

        # these are passed up to RenderBase
        # they should probably be moved to their own class
        # but I don't really have time for it
        # font-size in points
        self.font_size = 12

        # margin-width in inches
        self.margin_width = 0.5

        self.top_margin = 0.5
        self.bottom_margin = 0.5

        self.executive_summary = True

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update settings for resume and subsections."""
        super().update_from_dict(data_dict)
        _section = data_dict.get("section")
        if _section is None:
            return

        if "personal" in _section:
            self.personal_settings.update_from_dict(_section["personal"])

        if "education" in _section:
            self.education_settings.update_from_dict(_section["education"])

        if "certifications" in _section:
            self.certifications_settings.update_from_dict(_section["certifications"])

        if "experience" in _section:
            self.experience_settings.update_from_dict(_section["experience"])

        if "skills_matrix" in _section:
            self.skills_matrix_settings.update_from_dict(_section["skills_matrix"])

        if "executive_summary" in _section:
            self.executive_summary_settings.update_from_dict(
                _section["executive_summary"],
            )

    # this is the top-level, and has no section name
