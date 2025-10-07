class ResumeSettingsBase:
    """Base class for managing resume settings.

    This class provides a method to update the settings from a dictionary.

    Attributes:
        None

    Methods:
        update_from_dict(data_dict: dict | None = None) -> None
            Update the settings from a dictionary.

    """

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update the settings from a dictionary.

        Args:
            data_dict (dict | None): Dictionary containing the new settings. If None, no changes are made.

        Returns:
            None

        Notes:
            1. If data_dict is None, the method returns without making any changes.
            2. The method iterates over each key-value pair in data_dict.
            3. If the key is 'section', it is ignored to avoid unwanted updates.
            4. If the key exists as an attribute of the class instance, its value is updated.

        """
        if data_dict is None:
            return

        for key, value in data_dict.items():
            if key == "section":
                continue
            if hasattr(self, key):
                setattr(self, key, value)


class ResumePersonalSettings(ResumeSettingsBase):
    """Control what parts of a resume's personal section are rendered.

    Attributes:
        contact_info (bool): Include contact information.
        banner (bool): Include banner.
        visa_status (bool): Include visa status.
        websites (bool): Include websites.
        note (bool): Include note.
        name (bool): Include name.
        email (bool): Include email.
        phone (bool): Include phone number.
        location (bool): Include location.
        linkedin (bool): Include LinkedIn.
        github (bool): Include GitHub.
        website (bool): Include personal website.
        twitter (bool): Include Twitter.
        require_sponsorship (bool): Include sponsorship requirement.
        work_authorization (bool): Include work authorization status.

    Methods:
        __init__(default_init: bool = True) -> None
            Initialize all attributes to default_init.
        to_dict() -> dict
            Return settings as a dictionary.

    """

    def __init__(self, default_init: bool = True):
        """Initialize everything to default_init.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. All attributes are initialized to default_init.
            2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

        """
        self.contact_info = default_init
        self.banner = default_init
        self.visa_status = default_init
        self.websites = default_init
        self.note = default_init

        # contact info
        self.name = default_init
        self.email = default_init
        self.phone = default_init
        self.location = default_init

        # websites
        self.linkedin = default_init
        self.github = default_init
        self.website = default_init
        self.twitter = default_init

        # visa status
        self.require_sponsorship = default_init
        self.work_authorization = default_init

    def to_dict(self) -> dict:
        """Return settings as a dictionary.

        Returns:
            dict: Dictionary containing all settings with their respective boolean values.

        Notes:
            1. The method constructs and returns a dictionary mapping each attribute to its value.

        """
        return {
            "contact_info": self.contact_info,
            "banner": self.banner,
            "visa_status": self.visa_status,
            "websites": self.websites,
            "note": self.note,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "linkedin": self.linkedin,
            "github": self.github,
            "website": self.website,
            "twitter": self.twitter,
            "require_sponsorship": self.require_sponsorship,
            "work_authorization": self.work_authorization,
        }


class ResumeEducationSettings(ResumeSettingsBase):
    """Control what parts of a resume's education section are rendered.

    Attributes:
        degrees (bool): Render all degrees (default is True).
        school (bool): Render school name (default is True).
        degree (bool): Render degree name (default is True).
        start_date (bool): Render start date of degree (default is True).
        end_date (bool): Render end date of degree (default is True).
        gpa (bool): Render GPA (default is True).
        major (bool): Render major of study (default is True).

    Methods:
        __init__(default_init: bool = True) -> None
            Initialize all attributes to default_init.
        to_dict() -> dict
            Return a dictionary representation of the settings.

    """

    def __init__(self, default_init: bool = True):
        """Initialize everything to default_init.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. All attributes are initialized to default_init.
            2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

        """
        self.degrees = default_init  # render all degrees
        self.school = default_init
        self.degree = default_init  # render degree name
        self.start_date = default_init
        self.end_date = default_init
        self.gpa = default_init
        self.major = default_init

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings.

        Returns:
            dict: Dictionary containing all education settings with their respective boolean values.

        Notes:
            1. The method constructs and returns a dictionary mapping each attribute to its value.

        """
        return {
            "degrees": self.degrees,
            "school": self.school,
            "degree": self.degree,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "gpa": self.gpa,
            "major": self.major,
        }


class ResumeCertificationsSettings(ResumeSettingsBase):
    """Control what parts of a resume's certifications section are rendered.

    Attributes:
        name (bool): Whether to render the name of the certification.
        issuer (bool): Whether to render the issuer of the certification.
        issued (bool): Whether to render the date of issuance.
        expires (bool): Whether to render the expiration date of the certification.
        certification_id (bool): Whether to render the id of the certification.

    Methods:
        __init__(default_init: bool = True) -> None
            Initialize all attributes to True.
        to_dict() -> dict
            Return a dictionary representation of the object.

    """

    def __init__(self, default_init: bool = True):
        """Initialize everything to default_init.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. All attributes are initialized to default_init.
            2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

        """
        self.name = default_init
        self.issuer = default_init
        self.issued = default_init
        self.expires = default_init
        self.certification_id = default_init

    def to_dict(self) -> dict:
        """Return a dictionary representation of the object.

        Returns:
            dict: Dictionary containing all certification settings with their respective boolean values.

        Notes:
            1. The method constructs and returns a dictionary mapping each attribute to its value.

        """
        return {
            "name": self.name,
            "issuer": self.issuer,
            "issued": self.issued,
            "expires": self.expires,
            "certification_id": self.certification_id,
        }


class ResumeProjectsSettings(ResumeSettingsBase):
    """Control what parts of a resume's projects section are rendered.

    Attributes:
        overview (bool): Whether to include the project overview.
        description (bool): Whether to include the project description.
        skills (bool): Whether to include the skills used in the project.
        title (bool): Whether to include the project title.
        url (bool): Whether to include the project URL.
        url_description (bool): Whether to include the description for the project URL.
        start_date (bool): Whether to include the project start date.
        end_date (bool): Whether to include the project end date.

    Methods:
        __init__(default_init: bool)
            Initialize all attributes to True.
        to_dict() -> dict
            Return a dictionary representation of the class.

    """

    def __init__(self, default_init: bool = True):
        """Initialize everything to default_init.

        Args:
            default_init (bool): Default initialization value for all attributes.

        Returns:
            None

        Notes:
            1. All attributes are initialized to default_init.
            2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

        """
        self.overview = default_init
        self.description = default_init
        self.skills = default_init
        self.title = default_init
        self.url = default_init
        self.url_description = default_init
        self.start_date = default_init
        self.end_date = default_init

    def to_dict(self) -> dict:
        """Return a dictionary representation of the class.

        Returns:
            dict: Dictionary containing all project settings with their respective boolean values.

        Notes:
            1. The method constructs and returns a dictionary mapping each attribute to its value.

        """
        return {
            "overview": self.overview,
            "description": self.description,
            "skills": self.skills,
            "title": self.title,
            "url": self.url,
            "url_description": self.url_description,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }


class ResumeRolesSettings(ResumeSettingsBase):
    """Control what parts of a resume's roles section are rendered.

    Attributes:
        summary (bool): Whether to include the role summary.
        skills (bool): Whether to include the role skills.
        responsibilities (bool): Whether to include role responsibilities.
        reason_for_change (bool): Whether to include the reason for change.
        location (bool): Whether to include the role location.
        job_category (bool): Whether to include the role job category.
        employment_type (bool): Whether to include the role employment type.
        agency_name (bool): Whether to include the agency name.
        start_date (bool): Whether to include the role start date.
        end_date (bool): Whether to include the role end date.
        months_ago (int): Number of months ago the role ended.
        highlight_skills (bool): Whether to bold skills inline.
        include_situation (bool): Whether to include the situation in the role description.
        include_tasks (bool): Whether to include the tasks in the role description.

    Methods:
        __init__(default_init: bool = True) -> None
            Initialize everything to default_init.
        to_dict() -> dict
            Return a dictionary representation of the class.

    """

    def __init__(self, default_init: bool = True) -> None:
        """Initialize everything to default_init.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. All attributes are initialized to default_init.
            2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

        """
        # title is required
        self.summary = default_init
        self.skills = default_init
        self.responsibilities = default_init
        # basics
        self.reason_for_change = default_init
        self.location = default_init
        self.job_category = default_init
        self.employment_type = default_init
        self.agency_name = default_init
        self.start_date = default_init
        self.end_date = default_init
        self.months_ago = 0
        self.highlight_skills = default_init
        self.include_situation = default_init
        self.include_tasks = default_init

    def to_dict(self) -> dict:
        """Return a dictionary representation of the class.

        Returns:
            dict: Dictionary containing all role settings with their respective boolean values.

        Notes:
            1. The method constructs and returns a dictionary mapping each attribute to its value.

        """
        return {
            "summary": self.summary,
            "skills": self.skills,
            "responsibilities": self.responsibilities,
            "reason_for_change": self.reason_for_change,
            "location": self.location,
            "job_category": self.job_category,
            "employment_type": self.employment_type,
            "agency_name": self.agency_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "months_ago": self.months_ago,
            "highlight_skills": self.highlight_skills,
            "include_situation": self.include_situation,
            "include_tasks": self.include_tasks,
        }


class ResumeExperienceSettings(ResumeSettingsBase):
    """Control what parts of a resume's experience section are rendered.

    Attributes:
        roles (bool): Flag to include roles in the rendered experience section.
        roles_settings (ResumeRolesSettings): Settings for rendering roles in the experience section.
        projects (bool): Flag to include projects in the rendered experience section.
        projects_settings (ResumeProjectsSettings): Settings for rendering projects in the experience section.
        executive_summary (bool): Flag to include executive summary in the rendered experience section.
        executive_summary_settings (ResumeExecutiveSummarySettings): Settings for rendering executive summary in the experience section.
        skills_matrix (bool): Flag to include skills matrix in the rendered experience section.
        skills_matrix_settings (ResumeSkillsMatrixSettings): Settings for rendering skills matrix in the experience section.
        render_projects_first (bool): Flag to render projects before roles.

    Methods:
        update_from_dict(data_dict: dict | None = None) -> None
            Update settings for experience and subsections from a dictionary.
        to_dict() -> dict
            Convert settings for experience and subsections to a dictionary.

    """

    def __init__(self, default_init: bool = True) -> None:
        """Initialize all attributes to default_init and create settings objects.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. Initialize roles, projects, executive_summary, and skills_matrix to default_init.
            2. Create ResumeRolesSettings, ResumeProjectsSettings, ResumeExecutiveSummarySettings,
               and ResumeSkillsMatrixSettings objects.

        """
        self.roles = default_init
        self.roles_settings = ResumeRolesSettings(default_init=default_init)
        self.projects = default_init
        self.projects_settings = ResumeProjectsSettings(default_init=default_init)
        self.executive_summary = default_init
        self.executive_summary_settings = ResumeExecutiveSummarySettings()
        self.skills_matrix = default_init
        self.skills_matrix_settings = ResumeSkillsMatrixSettings()
        self.render_projects_first = False

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update settings for experience and subsections from a dictionary.

        Args:
            data_dict (dict | None): Dictionary containing settings for experience and subsections.

        Returns:
            None

        Notes:
            1. The method updates settings for subsections by extracting the 'section' key
               from the dictionary and applying updates to corresponding settings objects.
            2. The method calls the parent class's update_from_dict method to update base settings.

        """
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

    def to_dict(self) -> dict:
        """Convert settings for experience and subsections to a dictionary.

        Returns:
            dict: Dictionary containing settings for experience and subsections.

        Notes:
            1. The method constructs a dictionary with keys for roles, projects, executive_summary,
               skills_matrix, and render_projects_first, and their corresponding values.
            2. If the value for a key is True, the corresponding settings object is converted to a dictionary
               and added to the dictionary.

        """
        data_dict = {
            "roles": self.roles,
            "projects": self.projects,
            "executive_summary": self.executive_summary,
            "skills_matrix": self.skills_matrix,
            "render_projects_first": self.render_projects_first,
        }
        if self.roles:
            data_dict["roles"] = self.roles_settings.to_dict()
        if self.projects:
            data_dict["projects"] = self.projects_settings.to_dict()
        if self.executive_summary:
            data_dict["executive_summary"] = self.executive_summary_settings.to_dict()
        if self.skills_matrix:
            data_dict["skills_matrix"] = self.skills_matrix_settings.to_dict()
        return {"section": data_dict}


class ResumeExecutiveSummarySettings(ResumeSettingsBase):
    """Control settings for rendering the executive summary section of a resume.

    Attributes:
        categories (list[str]): List of categories to include in the summary.

    Methods:
        update_from_dict(data_dict: dict | None = None) -> None
            Update settings from a dictionary.
        to_dict() -> dict
            Return a dictionary representation of the settings.

    """

    def __init__(self) -> None:
        """Initialize everything to True.

        Returns:
            None

        Notes:
            1. Initialize categories as an empty list.

        """
        self.categories: list[str] = []

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Control what categories are rendered.

        Args:
            data_dict (dict | None): Dictionary containing settings for the executive summary.

        Returns:
            None

        Notes:
            1. The method updates settings from a dictionary.
            2. If categories are provided in the dictionary, split them into a list.

        """
        super().update_from_dict(data_dict)
        if self.categories:
            self.categories = self.categories.split("\n")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings.

        Returns:
            dict: Dictionary containing the categories as a string separated by newlines.

        Notes:
            1. The method returns a dictionary with categories joined by newlines.

        """
        return {"categories": "\n".join(self.categories) if self.categories else ""}


class ResumeSkillsMatrixSettings(ResumeSettingsBase):
    """Control what parts of a resume's skills matrix section are rendered.

    Attributes:
        skills (list[str]): List of skills to be rendered.
        all_skills (bool): Flag to indicate if all skills should be rendered.

    Methods:
        update_from_dict(data_dict: dict | None = None) -> None
            Update settings from a dictionary.
        to_dict() -> dict
            Return a dictionary representation of the settings.

    """

    def __init__(self) -> None:
        """Initialize everything.

        Returns:
            None

        Notes:
            1. Initialize skills as an empty list and all_skills as False.

        """
        self.skills: list[str] = []
        self.all_skills: bool = False

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Control what skills are rendered.

        Args:
            data_dict (dict | None): Dictionary containing settings for the skills matrix.

        Returns:
            None

        Notes:
            1. The method updates settings from a dictionary.
            2. If skills are provided, split the skills string into a list.

        """
        super().update_from_dict(data_dict)
        if self.skills:
            self.skills = self.skills.split("\n")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings.

        Returns:
            dict: Dictionary containing skills as a string separated by newlines and all_skills as a boolean.

        Notes:
            1. The method returns a dictionary with skills joined by newlines.

        """
        return {
            "skills": "\n".join(self.skills) if self.skills else "",
            "all_skills": self.all_skills,
        }


class ResumeRenderSettings(ResumeSettingsBase):
    """Control what parts of a resume are rendered.

    Attributes:
        personal_settings (ResumePersonalSettings): Settings for personal information.
        personal (bool): Flag to include personal information.
        education_settings (ResumeEducationSettings): Settings for education information.
        education (bool): Flag to include education information.
        certifications_settings (ResumeCertificationsSettings): Settings for certifications information.
        certifications (bool): Flag to include certifications information.
        experience_settings (ResumeExperienceSettings): Settings for experience information.
        experience (bool): Flag to include experience information.
        skills_matrix (bool): Flag to include skills matrix information.
        skills_matrix_settings (ResumeSkillsMatrixSettings): Settings for skills matrix information.
        executive_summary (bool): Flag to include executive summary information.
        executive_summary_settings (ResumeExecutiveSummarySettings): Settings for executive summary information.
        font_size (int): Font size in points.
        margin_width (float): Margin width in inches.
        top_margin (float): Top margin in inches.
        bottom_margin (float): Bottom margin in inches.

    Methods:
        update_from_dict(data_dict: dict | None = None) -> None
            Update settings for resume and subsections.
        to_dict() -> dict
            Convert settings for resume and subsections to a dictionary.

    """

    def __init__(self, default_init: bool = True):
        """Initialize all settings with appropriate objects.

        Args:
            default_init (bool): Default initialization value for all attributes. Defaults to True.

        Returns:
            None

        Notes:
            1. Initialize all settings with appropriate objects.
            2. The font_size is set to 12.
            3. The margin_width is set to 0.5.
            4. The top_margin is set to 0.5.
            5. The bottom_margin is set to 0.5.

        """
        self.personal_settings = ResumePersonalSettings(default_init=default_init)
        self.personal = default_init
        self.education_settings = ResumeEducationSettings(default_init=default_init)
        self.education = default_init
        self.certifications_settings = ResumeCertificationsSettings(
            default_init=default_init,
        )
        self.certifications = default_init
        self.experience_settings = ResumeExperienceSettings(default_init=default_init)
        self.experience = default_init
        self.skills_matrix = default_init
        self.skills_matrix_settings = ResumeSkillsMatrixSettings()
        self.executive_summary = default_init
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

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update settings for resume and subsections.

        Args:
            data_dict (dict | None): Dictionary containing data to update settings.

        Returns:
            None

        Notes:
            1. The method updates settings for subsections by extracting the 'section' key
               from the dictionary and applying updates to corresponding settings objects.
            2. The method calls the parent class's update_from_dict method to update base settings.

        """
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

    def to_dict(self) -> dict:
        """Convert settings for resume and subsections to a dictionary.

        Returns:
            dict: Dictionary containing all settings.

        Notes:
            1. The method constructs and returns a dictionary containing all settings,
               including subsection settings.

        """
        settings_dict = super().to_dict()
        settings_dict["section"] = {
            "personal": self.personal_settings.to_dict(),
            "education": self.education_settings.to_dict(),
            "certifications": self.certifications_settings.to_dict(),
            "experience": self.experience_settings.to_dict(),
            "skills_matrix": self.skills_matrix_settings.to_dict(),
            "executive_summary": self.executive_summary_settings.to_dict(),
        }
        settings_dict["font_size"] = self.font_size
        settings_dict["margin_width"] = self.margin_width
        settings_dict["top_margin"] = self.top_margin
        settings_dict["bottom_margin"] = self.bottom_margin
        settings_dict["executive_summary"] = self.executive_summary
        return settings_dict

    # this is the top-level, and has no section name
