class ResumeSettingsBase:
    """Base class for managing resume settings.

    This class provides a method to update the settings from a dictionary.

    Methods
    -------
    update_from_dict(data_dict: dict | None = None)
        Update the settings from a dictionary.

    Parameters
    ----------
        data_dict : dict | None, optional
            Dictionary containing the new settings. If None, no changes are made.

    Notes
    -----
        1. If data_dict is None, the method returns without making any changes.
        2. The method iterates over each key-value pair in data_dict.
        3. If the key is 'section', it is ignored to avoid unwanted updates.
        4. If the key exists as an attribute of the class instance,
            its value is updated.

    """

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
    """Control what parts of a resume's personal section are rendered.

    Attributes:
    1. contact_info (bool): Include contact information.
    2. banner (bool): Include banner.
    3. visa_status (bool): Include visa status.
    4. websites (bool): Include websites.
    5. note (bool): Include note.

    Contact Information Attributes:
    6. name (bool): Include name.
    7. email (bool): Include email.
    8. phone (bool): Include phone number.
    9. location (bool): Include location.

    Websites Attributes:
    10. linkedin (bool): Include LinkedIn.
    11. github (bool): Include GitHub.
    12. website (bool): Include personal website.
    13. twitter (bool): Include Twitter.

    Visa Status Attributes:
    14. require_sponsorship (bool): Include sponsorship requirement.
    15. work_authorization (bool): Include work authorization status.

    """

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

    def to_dict(self) -> dict:
        """Return settings as a dictionary."""
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

    Attributes
    ----------
    degrees : bool
        Render all degrees (default is True).
    school : bool
        Render school name (default is True).
    degree : bool
        Render degree name (default is True).
    start_date : bool
        Render start date of degree (default is True).
    end_date : bool
        Render end date of degree (default is True).
    gpa : bool
        Render GPA (default is True).
    major : bool
        Render major of study (default is True).

    Methods
    -------
    __init__()
        Initialize all attributes to True.

    Notes
    -----
    1. This class is used to control which parts of a resume's education
       section are rendered.
    2. Each attribute corresponds to a different part of the education
       section that can be rendered or not.
    3. By default, all attributes are set to True, meaning all parts of
       the education section will be rendered.
    4. To change which parts of the education section are rendered, set
       the corresponding attribute to False.

    """

    def __init__(self):
        """Initialize everything to True."""

        self.degrees = True  # render all degrees

        self.school = True
        self.degree = True  # render degree name
        self.start_date = True
        self.end_date = True
        self.gpa = True
        self.major = True

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings."""
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

    Attributes
    ----------
    name : bool
        Whether to render the name of the certification.
    issuer : bool
        Whether to render the issuer of the certification.
    issued : bool
        Whether to render the date of issuance.
    expires : bool
        Whether to render the expiration date of the certification.
    certification_id : bool
        Whether to render the id of the certification.

    Methods
    -------
    __init__()
        Initialize all attributes to True.
    to_dict()
        Return a dictionary representation of the object.

    """

    def __init__(self):
        """Initialize everything to True."""

        self.name = True
        self.issuer = True
        self.issued = True
        self.expires = True
        self.certification_id = True

    def to_dict(self) -> dict:
        """Return a dictionary representation of the object."""
        return {
            "name": self.name,
            "issuer": self.issuer,
            "issued": self.issued,
            "expires": self.expires,
            "certification_id": self.certification_id,
        }


class ResumeProjectsSettings(ResumeSettingsBase):
    """Control what parts of a resume's projects section are rendered.

    Parameters
    ----------
    None

    Attributes
    ----------
    overview : bool
        Whether to include the project overview.
    description : bool
        Whether to include the project description.
    skills : bool
        Whether to include the skills used in the project.
    title : bool
        Whether to include the project title.
    url : bool
        Whether to include the project URL.
    url_description : bool
        Whether to include the description for the project URL.
    start_date : bool
        Whether to include the project start date.
    end_date : bool
        Whether to include the project end date.

    Methods
    -------
    __init__()
        Initialize all attributes to True.
    to_dict()
        Return a dictionary representation of the class.

    Notes
    -----
    1. This class is used to control which parts of a resume's projects
       section are rendered.
    2. Each attribute corresponds to a different part of the project
       section that can be included or excluded from the rendered resume.
    3. The __init__ method initializes all attributes to True, meaning
       that all parts of the project section will be included by default.

    """

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

    def to_dict(self) -> dict:
        """Return a dictionary representation of the class."""

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

    Steps:
        1. Initialize the class with all attributes set to True.
        2. The title attribute is not included as it is required.

    """

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
        self.months_ago = 0

    def to_dict(self) -> dict:
        """Return a dictionary representation of the class."""
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
        }


class ResumeExperienceSettings(ResumeSettingsBase):
    """Control what parts of a resume's experience section are rendered.

    Parameters
    ----------
    None

    Attributes
    ----------
    roles : bool
        Flag to include roles in the rendered experience section.
    roles_settings : ResumeRolesSettings
        Settings for rendering roles in the experience section.
    projects : bool
        Flag to include projects in the rendered experience section.
    projects_settings : ResumeProjectsSettings
        Settings for rendering projects in the experience section.
    executive_summary : bool
        Flag to include executive summary in the rendered experience section.
    executive_summary_settings : ResumeExecutiveSummarySettings
        Settings for rendering executive summary in the experience section.
    skills_matrix : bool
        Flag to include skills matrix in the rendered experience section.
    skills_matrix_settings : ResumeSkillsMatrixSettings
        Settings for rendering skills matrix in the experience section.

    Methods
    -------
    update_from_dict(data_dict=None)
        Update settings for experience and subsections from a dictionary.

    """

    def __init__(self) -> None:
        """Initialize all attributes to True and create settings objects.

        Steps:
        1. Set roles, projects, executive_summary, and skills_matrix to True.
        2. Create ResumeRolesSettings, ResumeProjectsSettings,
           ResumeExecutiveSummarySettings, and ResumeSkillsMatrixSettings objects.
        """

        self.roles = True
        self.roles_settings = ResumeRolesSettings()
        self.projects = True
        self.projects_settings = ResumeProjectsSettings()
        self.executive_summary = True
        self.executive_summary_settings = ResumeExecutiveSummarySettings()
        self.skills_matrix = True
        self.skills_matrix_settings = ResumeSkillsMatrixSettings()

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Update settings for experience and subsections from a dictionary.

        Parameters
        ----------
        data_dict : dict, optional
            Dictionary containing settings for experience and subsections.

        Steps:
        1. Call the parent class's update_from_dict method.
        2. Extract the 'section' key from the dictionary.
        3. Update the settings for projects, roles, executive_summary,
           and skills_matrix if they exist in the 'section' key.

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

        Returns
        -------
        dict
            Dictionary containing settings for experience and subsections.

        Steps:
        1. Create a dictionary with keys for roles, projects, executive_summary,
        and skills_matrix, and their corresponding values.
        2. If the value for a key is True, convert the corresponding settings
        object to a dictionary and add it to the dictionary.
        3. Return the dictionary.

        """
        data_dict = {
            "roles": self.roles,
            "projects": self.projects,
            "executive_summary": self.executive_summary,
            "skills_matrix": self.skills_matrix,
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
        update_from_dict(data_dict): Update settings from a dictionary.

    1. Initialize categories as an empty list.
    2. Define a method to update settings from a dictionary.
    3. If categories are provided in the dictionary, split them into a list.

    """

    def __init__(self) -> None:
        """Initialize everything to True."""
        self.categories: list[str] = ""

    def update_from_dict(self, data_dict: dict | None = None) -> None:
        """Control what categories are rendered."""
        # categories and skills are kept as a single string, so we need to split them
        super().update_from_dict(data_dict)
        if self.categories:
            self.categories = self.categories.split("\n")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings."""
        return {"categories": "\n".join(self.categories) if self.categories else ""}


class ResumeSkillsMatrixSettings(ResumeSettingsBase):
    """Control what parts of a resume's skills matrix section are rendered.

    Attributes:
        skills (list[str]): List of skills to be rendered.
        all_skills (bool): Flag to indicate if all skills should be rendered.

    Methods:
        update_from_dict(data_dict): Update settings from a dictionary.

    1. Initialize skills as an empty list and all_skills as False.
    2. Call the parent class's update_from_dict method.
    3. If skills are provided, split the skills string into a list.

    """

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

    def to_dict(self) -> dict:
        """Return a dictionary representation of the settings."""
        return {
            "skills": "\n".join(self.skills) if self.skills else "",
            "all_skills": self.all_skills,
        }


class ResumeRenderSettings(ResumeSettingsBase):
    """Control what parts of a resume are rendered.

    Parameters
    ----------
    None

    Attributes
    ----------
    personal_settings : ResumePersonalSettings
        Settings for personal information.
    personal : bool
        Flag to include personal information.
    education_settings : ResumeEducationSettings
        Settings for education information.
    education : bool
        Flag to include education information.
    certifications_settings : ResumeCertificationsSettings
        Settings for certifications information.
    certifications : bool
        Flag to include certifications information.
    experience_settings : ResumeExperienceSettings
        Settings for experience information.
    experience : bool
        Flag to include experience information.
    skills_matrix : bool
        Flag to include skills matrix information.
    skills_matrix_settings : ResumeSkillsMatrixSettings
        Settings for skills matrix information.
    executive_summary : bool
        Flag to include executive summary information.
    executive_summary_settings : ResumeExecutiveSummarySettings
        Settings for executive summary information.
    font_size : int
        Font size in points.
    margin_width : float
        Margin width in inches.
    top_margin : float
        Top margin in inches.
    bottom_margin : float
        Bottom margin in inches.

    Methods
    -------
    update_from_dict(data_dict=None)
        Update settings for resume and subsections.

    """

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
        """Update settings for resume and subsections.

        Parameters
        ----------
        data_dict : dict, optional
            Dictionary containing data to update settings.

        Returns
        -------
        None

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

        Returns
        -------
        dict
            Dictionary containing all settings.

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
