from datetime import datetime, timedelta, timezone
from pathlib import Path

import docx.document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

from resume_writer.models.certifications import Certification, Certifications
from resume_writer.models.education import Degree, Education
from resume_writer.models.experience import (
    Experience,
    Project,
    Projects,
    Role,
    Roles,
)
from resume_writer.models.personal import Personal
from resume_writer.models.resume import Resume
from resume_writer.resume_render.render_settings import (
    ResumeCertificationsSettings,
    ResumeEducationSettings,
    ResumeExecutiveSummarySettings,
    ResumeExperienceSettings,
    ResumePersonalSettings,
    ResumeProjectsSettings,
    ResumeRenderSettings,
    ResumeRolesSettings,
    ResumeSkillsMatrixSettings,
)


class RenderBase:
    """Base class for rendering docx files.

    Used for common functionality between the different renderers,
    primarily error and warning collection.

    Attributes:
        errors (list): List of errors encountered during rendering.
        warnings (list): List of warnings encountered during rendering.
        document (docx.document.Document): The document object to render into.
        font_size (float): The font size used in the document, extracted from the Normal style.

    Methods:
        add_horizontal_line: Adds a horizontal line to a paragraph with optional offset.

    Notes:
        1. The class initializes error and warning lists.
        2. It sets up the document reference.
        3. It ensures the Normal style font size is set to 12pt if not already set.
        4. The font size is stored in the class for use by subclasses.

    """

    def __init__(self, document: docx.document.Document):
        """Initialize superclass.

        Args:
            document (docx.document.Document): The document object to render into.

        Returns:
            None

        Notes:
            1. Initialize errors and warnings lists.
            2. Store the document reference.
            3. Ensure the Normal style font size is set to 12pt if not already set.
            4. Store the font size from the Normal style in the class.
            5. Raise ValueError if the font size is not set.

        """
        self.errors = []
        self.warnings = []

        self.document = document

        _normal = self.document.styles["Normal"]
        _font = _normal.font

        # font size should always be set. Other classes use it for scaling.
        # If it isn't set, the other classes will fail.
        if not _font.size:
            _font.size = Pt(12)

        # put the font-size into the class, so subclasses easily use it
        if _normal.font.size:
            self.font_size = _normal.font.size.pt
        else:
            raise ValueError("Normal style font size not set.")

    def add_horizontal_line(self, paragraph: Paragraph, offset: int = 0) -> None:
        """Add a horizontal line to a paragraph with optional offset.

        Args:
            paragraph (docx.text.paragraph.Paragraph): The paragraph to add the line to.
            offset (int): The indentation offset in inches (default is 0).

        Returns:
            None

        Notes:
            1. Access the paragraph's XML element.
            2. Create a new paragraph border element.
            3. Configure the bottom border with single line style, size 6, space 1, and auto color.
            4. Append the border to the paragraph properties.
            5. Set left and right indentation of the paragraph based on the offset.

        """
        p = paragraph._element  # noqa: SLF001
        p_pr = p.get_or_add_pPr()
        p_borders = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "auto")
        p_borders.append(bottom)
        p_pr.append(p_borders)
        paragraph.paragraph_format.left_indent = Inches(offset)
        paragraph.paragraph_format.right_indent = Inches(offset)


class ResumeRenderBase(RenderBase):
    """Base class for rendering resumes.

    Attributes:
        settings (ResumeRenderSettings): Configuration settings for the resume.
        resume (Resume): The resume object containing the data to render.
        font_size (float): The font size used in the document, extracted from the Normal style.

    Methods:
        save: Saves the rendered document to a file.

    Notes:
        1. The class initializes with a document, resume, and optional settings.
        2. If no settings are provided, it defaults to a new ResumeRenderSettings instance.
        3. It sets up the document's Normal style spacing and font size.
        4. It configures document margins based on settings.
        5. The settings are stored in the instance.

    """

    def __init__(
        self,
        document: docx.document.Document,
        resume: Resume,
        settings: ResumeRenderSettings | None,
    ):
        """Initialize superclass.

        Args:
            document (docx.document.Document): The document object to render into.
            resume (Resume): The resume object containing the data to render.
            settings (ResumeRenderSettings | None): Configuration settings for the resume (optional).

        Returns:
            None

        Notes:
            1. Validate that resume is of type Resume and settings is of type ResumeRenderSettings or None.
            2. If settings is None, create a new ResumeRenderSettings instance.
            3. Call the parent constructor to initialize common attributes.
            4. Store the settings and resume objects.
            5. Configure the Normal style to have no space before or after paragraphs.
            6. Set the font size from settings if provided.
            7. Configure document margins based on settings (left, right, top, bottom).

        """
        assert isinstance(resume, Resume)
        assert isinstance(settings, ResumeRenderSettings) or settings is None

        if settings is None:
            settings = ResumeRenderSettings()

        super().__init__(document=document)

        self.settings = settings
        self.resume = resume

        _normal = self.document.styles["Normal"]

        _normal.paragraph_format.space_before = Pt(0)
        _normal.paragraph_format.space_after = Pt(0)

        _font = _normal.font

        if self.settings.font_size:
            _font.size = Pt(int(self.settings.font_size))

        # margins are set per-section
        _section = self.document.sections[0]

        if self.settings.margin_width:
            _section.left_margin = Inches(float(self.settings.margin_width))
            _section.right_margin = Inches(float(self.settings.margin_width))

        if self.settings.bottom_margin:
            _section.bottom_margin = Inches(float(self.settings.bottom_margin))

        if self.settings.top_margin:
            _section.top_margin = Inches(float(self.settings.top_margin))

    def save(self, path: Path) -> None:
        """Save the document to a file.

        Args:
            path (pathlib.Path): The file path to save the document to.

        Returns:
            None

        Notes:
            1. The document is saved to the specified path using the docx library.
            2. This operation writes to disk.

        """
        self.document.save(path)


class ResumeRenderPersonalBase(RenderBase):
    """Base class for rendering resume personal section.

    Attributes:
        settings (ResumePersonalSettings): Configuration settings for the personal section.
        personal (Personal): The personal information object to render.

    Methods:
        None

    Notes:
        1. The class initializes with a document, personal data, and settings.
        2. It validates the types of the inputs.
        3. If the document is a list of strings, it ensures all items are strings.
        4. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document | list[str],
        personal: Personal,
        settings: ResumePersonalSettings,
    ):
        """Initialize personal renderer.

        Args:
            document (docx.document.Document | list[str]): The document object or a list of strings.
            personal (Personal): The personal information object to render.
            settings (ResumePersonalSettings): Configuration settings for the personal section.

        Returns:
            None

        Notes:
            1. Validate that document is either a docx document or a list of strings.
            2. If document is a list of strings, validate all items are strings.
            3. Validate that personal is of type Personal.
            4. Validate that settings is of type ResumePersonalSettings.
            5. Call the parent constructor to initialize common attributes.

        """
        assert isinstance(document, (docx.document.Document, list))
        if isinstance(document, list):
            assert all(isinstance(item, str) for item in document)
        assert isinstance(personal, Personal)
        assert isinstance(settings, ResumePersonalSettings)

        super().__init__(document=document)

        self.settings = settings
        self.personal = personal


class ResumeRenderRolesBase(RenderBase):
    """Base class for rendering resume roles section.

    Attributes:
        _roles (Roles): The list of roles to render.
        settings (ResumeRolesSettings): Configuration settings for the roles section.

    Methods:
        roles: Property to get filtered roles based on settings.

    Notes:
        1. The class initializes with a document, roles, and settings.
        2. It validates the types of the inputs.
        3. It stores the roles and settings.
        4. The roles property filters roles older than the specified number of months.

    """

    def __init__(
        self,
        document: docx.document.Document,
        roles: Roles,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section.

        Args:
            document (docx.document.Document): The document object to render into.
            roles (Roles): The list of role objects to render.
            settings (ResumeRolesSettings): Configuration settings for the roles section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that roles is of type Roles.
            3. Validate that settings is of type ResumeRolesSettings.
            4. Store the roles and settings.

        """
        super().__init__(document=document)
        assert isinstance(roles, Roles)
        assert isinstance(settings, ResumeRolesSettings)

        self._roles = roles
        self.settings = settings

    @property
    def roles(self) -> list[Role]:
        """Return roles which have not been filtered out.

        Args:
            None

        Returns:
            list[Role]: A list of Role objects that are not older than the specified number of months.

        Notes:
            1. Initialize an empty list to store filtered roles.
            2. Iterate through each role in _roles.
            3. If months_ago is set and greater than 0, calculate the date threshold.
            4. If the role's end date is older than the threshold, skip it.
            5. Otherwise, add the role to the result list.
            6. Return the filtered list.

        """
        _ret_roles = []
        for _role in self._roles:
            # Check if the role is older than the specified number of months
            if self.settings.months_ago and int(self.settings.months_ago) > 0:
                _now = datetime.now(tz=timezone.utc)
                _end_date = _role.basics.end_date or _now
                _months_ago = _now - timedelta(days=int(self.settings.months_ago) * 30)
                if _end_date < _months_ago:
                    continue
            _ret_roles.append(_role)
        return _ret_roles


class ResumeRenderRoleBase(RenderBase):
    """Base class for rendering resume role section.

    Attributes:
        role (Role): The role object to render.
        settings (ResumeRolesSettings): Configuration settings for the role section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, role, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        role: Role,
        settings: ResumeRolesSettings,
    ):
        """Initialize the role section.

        Args:
            document (docx.document.Document): The document object to render into.
            role (Role): The role object to render.
            settings (ResumeRolesSettings): Configuration settings for the role section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that role is of type Role.
            3. Validate that settings is of type ResumeRolesSettings.
            4. Store the role and settings.

        """
        super().__init__(document=document)
        assert isinstance(role, Role)
        assert isinstance(settings, ResumeRolesSettings)

        self.role = role
        self.settings = settings


class ResumeRenderProjectsBase(RenderBase):
    """Base class for rendering resume projects section.

    Attributes:
        document (docx.document.Document): The document object to render into.
        projects (Projects): The list of project objects to render.
        settings (ResumeProjectsSettings): Configuration settings for the projects section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, projects, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        projects: Projects,
        settings: ResumeProjectsSettings,
    ):
        """Initialize the projects section.

        Args:
            document (docx.document.Document): The document object to render into.
            projects (Projects): The list of project objects to render.
            settings (ResumeProjectsSettings): Configuration settings for the projects section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that projects is of type Projects.
            3. Validate that settings is of type ResumeProjectsSettings.
            4. Store the document, projects, and settings.

        """
        super().__init__(document=document)
        assert isinstance(projects, Projects)
        assert isinstance(settings, ResumeProjectsSettings)

        self.document = document
        self.projects = projects
        self.settings = settings


class ResumeRenderProjectBase(RenderBase):
    """Base class for rendering resume project section.

    Attributes:
        document (docx.document.Document): The document object to render into.
        project (Project): The project object to render.
        settings (ResumeProjectsSettings): Configuration settings for the project section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, project, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        project: Project,
        settings: ResumeProjectsSettings,
    ):
        """Initialize the project section.

        Args:
            document (docx.document.Document): The document object to render into.
            project (Project): The project object to render.
            settings (ResumeProjectsSettings): Configuration settings for the project section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that project is of type Project.
            3. Validate that settings is of type ResumeProjectsSettings.
            4. Store the document, project, and settings.

        """
        super().__init__(document=document)
        assert isinstance(project, Project)
        assert isinstance(settings, ResumeProjectsSettings)

        self.document = document
        self.project = project
        self.settings = settings


class ResumeRenderExperienceBase(RenderBase):
    """Base class for rendering resume experience section.

    Attributes:
        experience (Experience): The experience object to render.
        document (docx.document.Document): The document object to render into.
        settings (ResumeRolesSettings): Configuration settings for the experience section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, experience, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeRolesSettings,
    ):
        """Initialize the roles section.

        Args:
            document (docx.document.Document): The document object to render into.
            experience (Experience): The experience object to render.
            settings (ResumeRolesSettings): Configuration settings for the experience section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that experience is of type Experience.
            3. Validate that settings is of type ResumeRolesSettings.
            4. Store the experience, document, and settings.

        """
        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeExperienceSettings)

        self.experience = experience
        self.document = document
        self.settings = settings


class ResumeRenderDegreeBase(RenderBase):
    """Base class for rendering a single degree.

    Attributes:
        degree (Degree): The degree object to render.
        settings (ResumeEducationSettings): Configuration settings for the degree section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, degree, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        degree: Degree,
        settings: ResumeEducationSettings,
    ):
        """Initialize the degree section.

        Args:
            document (docx.document.Document): The document object to render into.
            degree (Degree): The degree object to render.
            settings (ResumeEducationSettings): Configuration settings for the degree section.

        Returns:
            None

        Notes:
            1. Validate that degree is of type Degree.
            2. Validate that settings is of type ResumeEducationSettings.
            3. Call the parent constructor.
            4. Store the degree and settings.

        """
        assert isinstance(degree, Degree)
        assert isinstance(settings, ResumeEducationSettings)

        super().__init__(document=document)

        self.degree = degree
        self.settings = settings


class ResumeRenderEducationBase(RenderBase):
    """Base class for rendering resume education section.

    Attributes:
        education (Education): The education object to render.
        settings (ResumeEducationSettings): Configuration settings for the education section.
        document (docx.document.Document): The document object to render into.

    Methods:
        degrees: Method to render the degrees section of education.
        render: Method to render the education section.

    Notes:
        1. The class initializes with a document, education, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.
        4. The degrees method is not implemented in this base class.
        5. The render method is not implemented in this base class.

    """

    def __init__(
        self,
        document: docx.document.Document,
        education: Education,
        settings: ResumeEducationSettings,
    ):
        """Initialize the education rendering section.

        Args:
            document (docx.document.Document): The document object to render into.
            education (Education): The education object to render.
            settings (ResumeEducationSettings): Configuration settings for the education section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that education is of type Education.
            3. Validate that settings is of type ResumeEducationSettings.
            4. Store the education, settings, and document.

        """
        super().__init__(document=document)

        assert isinstance(education, Education)
        assert isinstance(settings, ResumeEducationSettings)

        self.education = education
        self.settings = settings

    def degrees(self) -> None:
        """Render degrees section of education.

        Args:
            None

        Returns:
            None

        Notes:
            1. This method is not implemented in the base class.
            2. It must be implemented by subclasses.

        """
        raise NotImplementedError

    def render(self) -> None:
        """Render education section.

        Args:
            None

        Returns:
            None

        Notes:
            1. This method is not implemented in the base class.
            2. It must be implemented by subclasses.

        """
        raise NotImplementedError


class ResumeRenderCertificationBase(RenderBase):
    """Base class for rendering a single certification.

    Attributes:
        certification (Certification): The certification object to render.
        settings (ResumeCertificationsSettings): Configuration settings for the certification section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, certification, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        certification: Certification,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize the certification section.

        Args:
            document (docx.document.Document): The document object to render into.
            certification (Certification): The certification object to render.
            settings (ResumeCertificationsSettings): Configuration settings for the certification section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that certification is of type Certification.
            3. Validate that settings is of type ResumeCertificationsSettings.
            4. Store the certification and settings.

        """
        super().__init__(document=document)

        assert isinstance(certification, Certification)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.certification = certification
        self.settings = settings


class ResumeRenderCertificationsBase(RenderBase):
    """Base class for rendering resume certifications section.

    Attributes:
        settings (ResumeCertificationsSettings): Configuration settings for the certifications section.
        certifications (Certifications): The list of certification objects to render.

    Methods:
        None

    Notes:
        1. The class initializes with a document, certifications, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        certifications: Certifications,
        settings: ResumeCertificationsSettings,
    ):
        """Initialize certification renderer.

        Args:
            document (docx.document.Document): The document object to render into.
            certifications (Certifications): The list of certification objects to render.
            settings (ResumeCertificationsSettings): Configuration settings for the certifications section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that certifications is of type Certifications.
            3. Validate that settings is of type ResumeCertificationsSettings.
            4. Store the settings and certifications.

        """
        super().__init__(document=document)

        assert isinstance(certifications, Certifications)
        assert isinstance(settings, ResumeCertificationsSettings)

        self.settings = settings
        self.certifications = certifications


class ResumeRenderExecutiveSummaryBase(RenderBase):
    """Base class for rendering resume executive summary section.

    Attributes:
        experience (Experience): The experience object containing data for the summary.
        document (docx.document.Document): The document object to render into.
        settings (ResumeExecutiveSummarySettings): Configuration settings for the summary section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, experience, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeExecutiveSummarySettings,
    ) -> None:
        """Initialize the executive summary section.

        Args:
            document (docx.document.Document): The document object to render into.
            experience (Experience): The experience object to extract summary data from.
            settings (ResumeExecutiveSummarySettings): Configuration settings for the summary section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that experience is of type Experience.
            3. Validate that settings is of type ResumeExecutiveSummarySettings.
            4. Store the experience, document, and settings.

        """
        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeExecutiveSummarySettings)
        self.experience = experience
        self.document = document
        self.settings = settings


class ResumeRenderSkillsMatrixBase(RenderBase):
    """Base class for rendering resume skills matrix section.

    Attributes:
        experience (Experience): The experience object containing data for the skills matrix.
        document (docx.document.Document): The document object to render into.
        settings (ResumeSkillsMatrixSettings): Configuration settings for the skills matrix section.

    Methods:
        None

    Notes:
        1. The class initializes with a document, experience, and settings.
        2. It validates the types of the inputs.
        3. It calls the parent constructor.

    """

    def __init__(
        self,
        document: docx.document.Document,
        experience: Experience,
        settings: ResumeSkillsMatrixSettings,
    ) -> None:
        """Initialize the skills matrix section.

        Args:
            document (docx.document.Document): The document object to render into.
            experience (Experience): The experience object to extract skills data from.
            settings (ResumeSkillsMatrixSettings): Configuration settings for the skills matrix section.

        Returns:
            None

        Notes:
            1. Call the parent constructor.
            2. Validate that experience is of type Experience.
            3. Validate that settings is of type ResumeSkillsMatrixSettings.
            4. Store the experience, document, and settings.

        """
        super().__init__(document=document)
        assert isinstance(experience, Experience)
        assert isinstance(settings, ResumeSkillsMatrixSettings)
        self.experience = experience
        self.document = document
        self.settings = settings
