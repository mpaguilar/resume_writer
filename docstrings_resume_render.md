# Docstrings Reference

===
# File: `docx_hyperlink.py`

## function: `get_or_create_hyperlink_style(d: Document) -> str`

Create a hyperlink style if one doesn't exist, or return existing style.

Args:
    d: The Document object to check or modify for the hyperlink style.

Returns:
    The name of the style used for hyperlinks, which is "Hyperlink".

Notes:
    1. Check if a style named "Hyperlink" already exists in the document.
    2. If not, create a new style named "Default Character Font" with default character formatting.
    3. The "Default Character Font" style is set to be the default font and is hidden.
    4. Create a new style named "Hyperlink" based on the "Default Character Font" style.
    5. Set the hyperlink style to be visible when used and apply blue color and underline to the font.
    6. Return the name "Hyperlink" as the style identifier.

---

## function: `add_hyperlink(paragraph: Paragraph, text: str, url: str) -> docx.oxml.shared.OxmlElement`

Create a hyperlink object and add it to the paragraph.

Args:
    paragraph: The Paragraph object to which the hyperlink will be added.
    text: The text to display as the hyperlink.
    url: The URL that the hyperlink will point to.

Returns:
    The OxmlElement representing the hyperlink, which is added to the paragraph.

Notes:
    1. Access the document part of the paragraph to manage relationships.
    2. Create a unique relationship ID for the hyperlink using the provided URL.
    3. Create an XML element for the hyperlink and set its relationship ID.
    4. Create a new run element to hold the hyperlink text.
    5. Set the text of the run to the provided display text.
    6. Apply the hyperlink style to the run by retrieving or creating it.
    7. Append the run element to the hyperlink XML element.
    8. Append the complete hyperlink element to the paragraph's XML content.
    9. Return the created hyperlink element.

---


===

===
# File: `__init__.py`


===

===
# File: `resume_render_base.py`

## function: `__init__(self: UnknownType, document: docx.document.Document) -> UnknownType`

Initialize superclass.

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

---

## function: `add_horizontal_line(self: UnknownType, paragraph: Paragraph, offset: int) -> None`

Add a horizontal line to a paragraph with optional offset.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings | None) -> UnknownType`

Initialize superclass.

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

---

## function: `save(self: UnknownType, path: Path) -> None`

Save the document to a file.

Args:
    path (pathlib.Path): The file path to save the document to.

Returns:
    None

Notes:
    1. The document is saved to the specified path using the docx library.
    2. This operation writes to disk.

---

## function: `__init__(self: UnknownType, document: docx.document.Document | list[str], personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize personal renderer.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

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

---

## function: `roles(self: UnknownType) -> list[Role]`

Return roles which have not been filtered out.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize the role section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the projects section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the project section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the degree section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the education rendering section.

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

---

## function: `degrees(self: UnknownType) -> None`

Render degrees section of education.

Args:
    None

Returns:
    None

Notes:
    1. This method is not implemented in the base class.
    2. It must be implemented by subclasses.

---

## function: `render(self: UnknownType) -> None`

Render education section.

Args:
    None

Returns:
    None

Notes:
    1. This method is not implemented in the base class.
    2. It must be implemented by subclasses.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the certification section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize certification renderer.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize the executive summary section.

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

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings) -> None`

Initialize the skills matrix section.

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

---

## `RenderBase` class

Base class for rendering docx files.

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

---
## method: `RenderBase.__init__(self: UnknownType, document: docx.document.Document) -> UnknownType`

Initialize superclass.

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

---
## method: `RenderBase.add_horizontal_line(self: UnknownType, paragraph: Paragraph, offset: int) -> None`

Add a horizontal line to a paragraph with optional offset.

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

---
## `ResumeRenderBase` class

Base class for rendering resumes.

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

---
## method: `ResumeRenderBase.__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings | None) -> UnknownType`

Initialize superclass.

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

---
## method: `ResumeRenderBase.save(self: UnknownType, path: Path) -> None`

Save the document to a file.

Args:
    path (pathlib.Path): The file path to save the document to.

Returns:
    None

Notes:
    1. The document is saved to the specified path using the docx library.
    2. This operation writes to disk.

---
## `ResumeRenderPersonalBase` class

Base class for rendering resume personal section.

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

---
## method: `ResumeRenderPersonalBase.__init__(self: UnknownType, document: docx.document.Document | list[str], personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize personal renderer.

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

---
## `ResumeRenderRolesBase` class

Base class for rendering resume roles section.

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

---
## method: `ResumeRenderRolesBase.__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

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

---
## method: `ResumeRenderRolesBase.roles(self: UnknownType) -> list[Role]`

Return roles which have not been filtered out.

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

---
## `ResumeRenderRoleBase` class

Base class for rendering resume role section.

Attributes:
    role (Role): The role object to render.
    settings (ResumeRolesSettings): Configuration settings for the role section.

Methods:
    None

Notes:
    1. The class initializes with a document, role, and settings.
    2. It validates the types of the inputs.
    3. It calls the parent constructor.

---
## method: `ResumeRenderRoleBase.__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize the role section.

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

---
## `ResumeRenderProjectsBase` class

Base class for rendering resume projects section.

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

---
## method: `ResumeRenderProjectsBase.__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the projects section.

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

---
## `ResumeRenderProjectBase` class

Base class for rendering resume project section.

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

---
## method: `ResumeRenderProjectBase.__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the project section.

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

---
## `ResumeRenderExperienceBase` class

Base class for rendering resume experience section.

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

---
## method: `ResumeRenderExperienceBase.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

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

---
## `ResumeRenderDegreeBase` class

Base class for rendering a single degree.

Attributes:
    degree (Degree): The degree object to render.
    settings (ResumeEducationSettings): Configuration settings for the degree section.

Methods:
    None

Notes:
    1. The class initializes with a document, degree, and settings.
    2. It validates the types of the inputs.
    3. It calls the parent constructor.

---
## method: `ResumeRenderDegreeBase.__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the degree section.

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

---
## `ResumeRenderEducationBase` class

Base class for rendering resume education section.

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

---
## method: `ResumeRenderEducationBase.__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the education rendering section.

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

---
## method: `ResumeRenderEducationBase.degrees(self: UnknownType) -> None`

Render degrees section of education.

Args:
    None

Returns:
    None

Notes:
    1. This method is not implemented in the base class.
    2. It must be implemented by subclasses.

---
## method: `ResumeRenderEducationBase.render(self: UnknownType) -> None`

Render education section.

Args:
    None

Returns:
    None

Notes:
    1. This method is not implemented in the base class.
    2. It must be implemented by subclasses.

---
## `ResumeRenderCertificationBase` class

Base class for rendering a single certification.

Attributes:
    certification (Certification): The certification object to render.
    settings (ResumeCertificationsSettings): Configuration settings for the certification section.

Methods:
    None

Notes:
    1. The class initializes with a document, certification, and settings.
    2. It validates the types of the inputs.
    3. It calls the parent constructor.

---
## method: `ResumeRenderCertificationBase.__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the certification section.

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

---
## `ResumeRenderCertificationsBase` class

Base class for rendering resume certifications section.

Attributes:
    settings (ResumeCertificationsSettings): Configuration settings for the certifications section.
    certifications (Certifications): The list of certification objects to render.

Methods:
    None

Notes:
    1. The class initializes with a document, certifications, and settings.
    2. It validates the types of the inputs.
    3. It calls the parent constructor.

---
## method: `ResumeRenderCertificationsBase.__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize certification renderer.

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

---
## `ResumeRenderExecutiveSummaryBase` class

Base class for rendering resume executive summary section.

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

---
## method: `ResumeRenderExecutiveSummaryBase.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize the executive summary section.

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

---
## `ResumeRenderSkillsMatrixBase` class

Base class for rendering resume skills matrix section.

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

---
## method: `ResumeRenderSkillsMatrixBase.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings) -> None`

Initialize the skills matrix section.

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

---

===

===
# File: `render_settings.py`

## function: `update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update the settings from a dictionary.

---

## function: `__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---

## function: `to_dict(self: UnknownType) -> dict`

Return settings as a dictionary.

---

## function: `__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---

## function: `__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the object.

---

## function: `__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the class.

---

## function: `__init__(self: UnknownType, default_init: bool) -> None`

Initialize everything to default_init.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the class.

---

## function: `__init__(self: UnknownType, default_init: bool) -> None`

Initialize all attributes to default_init and create settings objects.

---

## function: `update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update settings for experience and subsections from a dictionary.

---

## function: `to_dict(self: UnknownType) -> dict`

Convert settings for experience and subsections to a dictionary.

---

## function: `__init__(self: UnknownType) -> None`

Initialize everything to True.

---

## function: `update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Control what categories are rendered.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---

## function: `__init__(self: UnknownType) -> None`

Initialize everything.
Set all_skills to False, because we don't usually want that.

---

## function: `update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Control what skills are rendered.

---

## function: `to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---

## function: `__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize all settings with appropriate objects.

---

## function: `update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update settings for resume and subsections.

---

## function: `to_dict(self: UnknownType) -> dict`

Convert settings for resume and subsections to a dictionary.

---

## `ResumeSettingsBase` class

Base class for managing resume settings.

This class provides a method to update the settings from a dictionary.

Methods
-------
update_from_dict(data_dict: dict | None = None)
    Update the settings from a dictionary.

Parameters
----------
    data_dict : dict | None, optional
        Dictionary containing the new settings. If None, no changes are made.

Returns
-------
    None

Notes
-----
    1. If data_dict is None, the method returns without making any changes.
    2. The method iterates over each key-value pair in data_dict.
    3. If the key is 'section', it is ignored to avoid unwanted updates.
    4. If the key exists as an attribute of the class instance,
        its value is updated.

---
## method: `ResumeSettingsBase.update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update the settings from a dictionary.

---
## `ResumePersonalSettings` class

Control what parts of a resume's personal section are rendered.

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

Methods
-------
__init__(default_init: bool = True)
    Initialize all attributes to default_init.

to_dict() -> dict
    Return settings as a dictionary.

Parameters
----------
    default_init : bool, optional
        Default initialization value for all attributes. Defaults to True.

Returns
-------
    dict
        Dictionary containing all settings with their respective boolean values.

Notes
-----
    1. All attributes are initialized to default_init.
    2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

---
## method: `ResumePersonalSettings.__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---
## method: `ResumePersonalSettings.to_dict(self: UnknownType) -> dict`

Return settings as a dictionary.

---
## `ResumeEducationSettings` class

Control what parts of a resume's education section are rendered.

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
__init__(default_init: bool = True)
    Initialize all attributes to default_init.

to_dict() -> dict
    Return a dictionary representation of the settings.

Parameters
----------
    default_init : bool, optional
        Default initialization value for all attributes. Defaults to True.

Returns
-------
    dict
        Dictionary containing all education settings with their respective boolean values.

Notes
-----
    1. All attributes are initialized to default_init.
    2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

---
## method: `ResumeEducationSettings.__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---
## method: `ResumeEducationSettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---
## `ResumeCertificationsSettings` class

Control what parts of a resume's certifications section are rendered.

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
__init__(default_init: bool = True)
    Initialize all attributes to True.

to_dict() -> dict
    Return a dictionary representation of the object.

Parameters
----------
    default_init : bool, optional
        Default initialization value for all attributes. Defaults to True.

Returns
-------
    dict
        Dictionary containing all certification settings with their respective boolean values.

Notes
-----
    1. All attributes are initialized to default_init.
    2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

---
## method: `ResumeCertificationsSettings.__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---
## method: `ResumeCertificationsSettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the object.

---
## `ResumeProjectsSettings` class

Control what parts of a resume's projects section are rendered.

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
__init__(default_init: bool)
    Initialize all attributes to True.

to_dict() -> dict
    Return a dictionary representation of the class.

Parameters
----------
    default_init : bool
        Default initialization value for all attributes.

Returns
-------
    dict
        Dictionary containing all project settings with their respective boolean values.

Notes
-----
    1. All attributes are initialized to default_init.
    2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

---
## method: `ResumeProjectsSettings.__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize everything to default_init.

---
## method: `ResumeProjectsSettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the class.

---
## `ResumeRolesSettings` class

Control what parts of a resume's roles section are rendered.

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
    highlight_skills (bool): Whether to bold skills inline.

Methods
-------
__init__(default_init: bool = True)
    Initialize everything to default_init.

to_dict() -> dict
    Return a dictionary representation of the class.

Parameters
----------
    default_init : bool, optional
        Default initialization value for all attributes. Defaults to True.

Returns
-------
    dict
        Dictionary containing all role settings with their respective boolean values.

Notes
-----
    1. All attributes are initialized to default_init.
    2. The to_dict method constructs and returns a dictionary mapping each attribute to its value.

---
## method: `ResumeRolesSettings.__init__(self: UnknownType, default_init: bool) -> None`

Initialize everything to default_init.

---
## method: `ResumeRolesSettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the class.

---
## `ResumeExperienceSettings` class

Control what parts of a resume's experience section are rendered.

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
update_from_dict(data_dict: dict | None = None) -> None
    Update settings for experience and subsections from a dictionary.

to_dict() -> dict
    Convert settings for experience and subsections to a dictionary.

Parameters
----------
    data_dict : dict | None, optional
        Dictionary containing settings for experience and subsections.

Returns
-------
    dict
        Dictionary containing settings for experience and subsections.

Notes
-----
    1. Initialize roles, projects, executive_summary, and skills_matrix to default_init.
    2. Create ResumeRolesSettings, ResumeProjectsSettings, ResumeExecutiveSummarySettings,
       and ResumeSkillsMatrixSettings objects.
    3. The update_from_dict method updates settings for subsections by extracting the 'section' key
       from the dictionary and applying updates to corresponding settings objects.
    4. The to_dict method constructs a dictionary with keys for roles, projects, executive_summary,
       and skills_matrix, and their corresponding values. If the value for a key is True,
       the corresponding settings object is converted to a dictionary and added to the dictionary.

---
## method: `ResumeExperienceSettings.__init__(self: UnknownType, default_init: bool) -> None`

Initialize all attributes to default_init and create settings objects.

---
## method: `ResumeExperienceSettings.update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update settings for experience and subsections from a dictionary.

---
## method: `ResumeExperienceSettings.to_dict(self: UnknownType) -> dict`

Convert settings for experience and subsections to a dictionary.

---
## `ResumeExecutiveSummarySettings` class

Control settings for rendering the executive summary section of a resume.

Attributes:
    categories (list[str]): List of categories to include in the summary.

Methods:
    update_from_dict(data_dict: dict | None = None) -> None
        Update settings from a dictionary.

to_dict() -> dict
    Return a dictionary representation of the settings.

Parameters
----------
    data_dict : dict | None, optional
        Dictionary containing settings for the executive summary.

Returns
-------
    dict
        Dictionary containing the categories as a string separated by newlines.

Notes
-----
    1. Initialize categories as an empty list.
    2. The update_from_dict method updates settings from a dictionary.
    3. If categories are provided in the dictionary, split them into a list.
    4. The to_dict method returns a dictionary with categories joined by newlines.

---
## method: `ResumeExecutiveSummarySettings.__init__(self: UnknownType) -> None`

Initialize everything to True.

---
## method: `ResumeExecutiveSummarySettings.update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Control what categories are rendered.

---
## method: `ResumeExecutiveSummarySettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---
## `ResumeSkillsMatrixSettings` class

Control what parts of a resume's skills matrix section are rendered.

Attributes:
    skills (list[str]): List of skills to be rendered.
    all_skills (bool): Flag to indicate if all skills should be rendered.

Methods:
    update_from_dict(data_dict: dict | None = None) -> None
        Update settings from a dictionary.

to_dict() -> dict
    Return a dictionary representation of the settings.

Parameters
----------
    data_dict : dict | None, optional
        Dictionary containing settings for the skills matrix.

Returns
-------
    dict
        Dictionary containing skills as a string separated by newlines and all_skills as a boolean.

Notes
-----
    1. Initialize skills as an empty list and all_skills as False.
    2. The update_from_dict method updates settings from a dictionary.
    3. If skills are provided, split the skills string into a list.
    4. The to_dict method returns a dictionary with skills joined by newlines.

---
## method: `ResumeSkillsMatrixSettings.__init__(self: UnknownType) -> None`

Initialize everything.
Set all_skills to False, because we don't usually want that.

---
## method: `ResumeSkillsMatrixSettings.update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Control what skills are rendered.

---
## method: `ResumeSkillsMatrixSettings.to_dict(self: UnknownType) -> dict`

Return a dictionary representation of the settings.

---
## `ResumeRenderSettings` class

Control what parts of a resume are rendered.

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
update_from_dict(data_dict: dict | None = None) -> None
    Update settings for resume and subsections.

to_dict() -> dict
    Convert settings for resume and subsections to a dictionary.

Parameters
----------
    data_dict : dict | None, optional
        Dictionary containing data to update settings.

Returns
-------
    dict
        Dictionary containing all settings.

Notes
-----
    1. Initialize all settings with appropriate objects.
    2. The update_from_dict method updates settings for subsections by extracting the 'section' key
       from the dictionary and applying updates to corresponding settings objects.
    3. The to_dict method constructs and returns a dictionary containing all settings,
       including subsection settings.

---
## method: `ResumeRenderSettings.__init__(self: UnknownType, default_init: bool) -> UnknownType`

Initialize all settings with appropriate objects.

---
## method: `ResumeRenderSettings.update_from_dict(self: UnknownType, data_dict: dict | None) -> None`

Update settings for resume and subsections.

---
## method: `ResumeRenderSettings.to_dict(self: UnknownType) -> dict`

Convert settings for resume and subsections to a dictionary.

---

===

===
# File: `resume_render_text_base.py`

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None) -> UnknownType`

Initialize superclass.

---

## function: `save(self: UnknownType, path: Path) -> None`

Save the document to the given path.

Args:
    path (Path): The file system path to save the document.

Returns:
    None

Notes:
    1. Opens the file at the given path in write mode.
    2. Writes the document's text content to the file.
    3. Closes the file.

---

## function: `add_error(self: UnknownType, error: str) -> None`

Add an error to the list of errors.

Args:
    error (str): The error message to add.

Returns:
    None

Notes:
    1. Appends the error message to the errors list.

---

## function: `add_warning(self: UnknownType, warning: str) -> None`

Add a warning to the list of warnings.

Args:
    warning (str): The warning message to add.

Returns:
    None

Notes:
    1. Appends the warning message to the warnings list.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None, resume: Resume, settings: ResumeRenderSettings | None) -> UnknownType`

Initialize superclass.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, personal: Personal, template_name: str, settings: ResumePersonalSettings) -> UnknownType`

Initialize personal renderer.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None, roles: Roles, template_name: str, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

---

## function: `roles(self: UnknownType) -> list[Role]`

Return roles which have not been filtered out.

Returns:
    list[Role]: A list of roles that are not older than the specified number of months.

Notes:
    1. Initializes an empty list to store filtered roles.
    2. Iterates over each role in the _roles list.
    3. If the settings specify a number of months ago, checks if the role's end date is older than that time.
    4. If the role is older than the specified time, skips it.
    5. Otherwise, adds the role to the filtered list.
    6. Returns the filtered list of roles.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, projects: Projects, template_name: str, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the projects section.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, experience: Experience, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

---

## function: `__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, education: Education, template_name: str, settings: ResumeEducationSettings) -> UnknownType`

Initialize the education rendering section.

---

## function: `degrees(self: UnknownType) -> None`

Render degrees section of education.

Returns:
    None

Notes:
    1. This method is currently a placeholder and not implemented.

---

## function: `render(self: UnknownType) -> None`

Render education section.

Returns:
    None

Notes:
    1. This method is currently a placeholder and not implemented.

---

## function: `__init__(self: UnknownType, document: str, certifications: Certifications, jinja_env: Environment, template_name: str, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize certification renderer.

---

## function: `__init__(self: UnknownType, document: str, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize the executive summary section.

---

## function: `__init__(self: UnknownType, document: str, experience: Experience, settings: ResumeSkillsMatrixSettings) -> None`

Initialize the skills matrix section.

---

## `RenderBase` class

Base class for rendering HTML files.

Used for common functionality between the different renderers,
primarily error and warning collection.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.

Attributes:
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.

Notes:
    1. Initializes the errors and warnings lists as empty.
    2. Validates that the document is an instance of TextDoc.
    3. Validates that jinja_env is either None or an instance of Environment.
    4. Assigns the provided document and jinja_env to instance attributes.

---
## method: `RenderBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None) -> UnknownType`

Initialize superclass.

---
## method: `RenderBase.save(self: UnknownType, path: Path) -> None`

Save the document to the given path.

Args:
    path (Path): The file system path to save the document.

Returns:
    None

Notes:
    1. Opens the file at the given path in write mode.
    2. Writes the document's text content to the file.
    3. Closes the file.

---
## method: `RenderBase.add_error(self: UnknownType, error: str) -> None`

Add an error to the list of errors.

Args:
    error (str): The error message to add.

Returns:
    None

Notes:
    1. Appends the error message to the errors list.

---
## method: `RenderBase.add_warning(self: UnknownType, warning: str) -> None`

Add a warning to the list of warnings.

Args:
    warning (str): The warning message to add.

Returns:
    None

Notes:
    1. Appends the warning message to the warnings list.

---
## `ResumeRenderBase` class

Base class for rendering resumes.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.
    resume (Resume): The resume data to be rendered.
    settings (ResumeRenderSettings | None): The rendering settings for the resume.

Attributes:
    settings (ResumeRenderSettings): The rendering settings for the resume.
    resume (Resume): The resume data to be rendered.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.

Notes:
    1. Validates that resume is an instance of Resume.
    2. Validates that settings is either None or an instance of ResumeRenderSettings.
    3. Validates that document is an instance of TextDoc.
    4. Validates that jinja_env is either None or an instance of Environment.
    5. If settings is None, initializes settings with a new ResumeRenderSettings instance.
    6. Calls the superclass constructor to initialize common attributes.

---
## method: `ResumeRenderBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None, resume: Resume, settings: ResumeRenderSettings | None) -> UnknownType`

Initialize superclass.

---
## `ResumeRenderPersonalBase` class

Base class for rendering resume personal section.

This class handles rendering of personal information such as name, contact details, and profile summary.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    personal (Personal): The personal data to be rendered.
    template_name (str): The name of the Jinja2 template to use for rendering.
    settings (ResumePersonalSettings): The rendering settings for the personal section.

Attributes:
    settings (ResumePersonalSettings): The rendering settings for the personal section.
    personal (Personal): The personal data to be rendered.
    template (Template | None): The Jinja2 template for rendering, if template_name is provided.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.

Notes:
    1. Validates that document is an instance of TextDoc.
    2. Validates that personal is an instance of Personal.
    3. Validates that settings is an instance of ResumePersonalSettings.
    4. Validates that template_name is a string.
    5. Calls the superclass constructor to initialize common attributes.
    6. Assigns the provided settings and personal data to instance attributes.
    7. If template_name is provided, loads the corresponding Jinja2 template.

---
## method: `ResumeRenderPersonalBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, personal: Personal, template_name: str, settings: ResumePersonalSettings) -> UnknownType`

Initialize personal renderer.

---
## `ResumeRenderRolesBase` class

Base class for rendering resume roles section.

This class handles filtering and rendering of job roles based on time constraints.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.
    roles (Roles): The list of job roles to be rendered.
    template_name (str): The name of the Jinja2 template to use for rendering.
    settings (ResumeRolesSettings): The rendering settings for the roles section.

Attributes:
    _roles (Roles): The list of job roles to be rendered.
    settings (ResumeRolesSettings): The rendering settings for the roles section.
    template (Template | None): The Jinja2 template for rendering, if template_name is provided.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment | None): The Jinja2 environment for template rendering.

Notes:
    1. Validates that document is an instance of TextDoc.
    2. Validates that roles is an instance of Roles.
    3. Validates that settings is an instance of ResumeRolesSettings.
    4. Validates that template_name is a string.
    5. Validates that jinja_env is either None or an instance of Environment.
    6. Calls the superclass constructor to initialize common attributes.
    7. Assigns the provided roles and settings to instance attributes.
    8. If template_name is provided, loads the corresponding Jinja2 template.

Returns:
    list[Role]: A list of roles that have not been filtered out based on the time constraint.

---
## method: `ResumeRenderRolesBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment | None, roles: Roles, template_name: str, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

---
## method: `ResumeRenderRolesBase.roles(self: UnknownType) -> list[Role]`

Return roles which have not been filtered out.

Returns:
    list[Role]: A list of roles that are not older than the specified number of months.

Notes:
    1. Initializes an empty list to store filtered roles.
    2. Iterates over each role in the _roles list.
    3. If the settings specify a number of months ago, checks if the role's end date is older than that time.
    4. If the role is older than the specified time, skips it.
    5. Otherwise, adds the role to the filtered list.
    6. Returns the filtered list of roles.

---
## `ResumeRenderProjectsBase` class

Base class for rendering resume projects section.

This class handles rendering of projects based on provided settings.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    projects (Projects): The list of projects to be rendered.
    template_name (str): The name of the Jinja2 template to use for rendering.
    settings (ResumeProjectsSettings): The rendering settings for the projects section.

Attributes:
    projects (Projects): The list of projects to be rendered.
    settings (ResumeProjectsSettings): The rendering settings for the projects section.
    template (Template | None): The Jinja2 template for rendering, if template_name is provided.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.

Notes:
    1. Validates that document is an instance of TextDoc.
    2. Validates that projects is an instance of Projects.
    3. Validates that settings is an instance of ResumeProjectsSettings.
    4. Validates that template_name is a string.
    5. Validates that jinja_env is either None or an instance of Environment.
    6. Calls the superclass constructor to initialize common attributes.
    7. Assigns the provided projects and settings to instance attributes.
    8. If template_name is provided, loads the corresponding Jinja2 template.

---
## method: `ResumeRenderProjectsBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, projects: Projects, template_name: str, settings: ResumeProjectsSettings) -> UnknownType`

Initialize the projects section.

---
## `ResumeRenderExperienceBase` class

Base class for rendering resume experience section.

This class handles rendering of experience sections, including roles.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    experience (Experience): The experience data to be rendered.
    settings (ResumeRolesSettings): The rendering settings for the roles section.

Attributes:
    experience (Experience): The experience data to be rendered.
    settings (ResumeRolesSettings): The rendering settings for the roles section.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.

Notes:
    1. Validates that experience is an instance of Experience.
    2. Validates that settings is an instance of ResumeExperienceSettings.
    3. Validates that jinja_env is either None or an instance of Environment.
    4. Validates that document is an instance of TextDoc.
    5. Calls the superclass constructor to initialize common attributes.
    6. Assigns the provided experience and settings to instance attributes.

---
## method: `ResumeRenderExperienceBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, experience: Experience, settings: ResumeRolesSettings) -> UnknownType`

Initialize the roles section.

---
## `ResumeRenderEducationBase` class

Base class for rendering resume education section.

This class handles rendering of educational qualifications.

Args:
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    education (Education): The education data to be rendered.
    template_name (str): The name of the Jinja2 template to use for rendering.
    settings (ResumeEducationSettings): The rendering settings for the education section.

Attributes:
    education (Education): The education data to be rendered.
    settings (ResumeEducationSettings): The rendering settings for the education section.
    template (Template | None): The Jinja2 template for rendering, if template_name is provided.
    document (TextDoc): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.

Notes:
    1. Validates that education is an instance of Education.
    2. Validates that settings is an instance of ResumeEducationSettings.
    3. Validates that template_name is a string.
    4. Validates that jinja_env is either None or an instance of Environment.
    5. Calls the superclass constructor to initialize common attributes.
    6. Assigns the provided education and settings to instance attributes.
    7. If template_name is provided, loads the corresponding Jinja2 template.

---
## method: `ResumeRenderEducationBase.__init__(self: UnknownType, document: TextDoc, jinja_env: Environment, education: Education, template_name: str, settings: ResumeEducationSettings) -> UnknownType`

Initialize the education rendering section.

---
## method: `ResumeRenderEducationBase.degrees(self: UnknownType) -> None`

Render degrees section of education.

Returns:
    None

Notes:
    1. This method is currently a placeholder and not implemented.

---
## method: `ResumeRenderEducationBase.render(self: UnknownType) -> None`

Render education section.

Returns:
    None

Notes:
    1. This method is currently a placeholder and not implemented.

---
## `ResumeRenderCertificationsBase` class

Base class for rendering resume certifications section.

This class handles rendering of certifications based on provided settings.

Args:
    document (str): The text document to be rendered.
    certifications (Certifications): The certifications data to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    template_name (str): The name of the Jinja2 template to use for rendering.
    settings (ResumeCertificationsSettings): The rendering settings for the certifications section.

Attributes:
    settings (ResumeCertificationsSettings): The rendering settings for the certifications section.
    certifications (Certifications): The certifications data to be rendered.
    template (Template | None): The Jinja2 template for rendering, if template_name is provided.
    document (str): The text document to be rendered.
    jinja_env (Environment): The Jinja2 environment for template rendering.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.

Notes:
    1. Validates that certifications is an instance of Certifications.
    2. Validates that settings is an instance of ResumeCertificationsSettings.
    3. Validates that template_name is a string.
    4. Validates that jinja_env is either None or an instance of Environment.
    5. Calls the superclass constructor to initialize common attributes.
    6. Assigns the provided settings and certifications to instance attributes.
    7. If template_name is provided, loads the corresponding Jinja2 template.

---
## method: `ResumeRenderCertificationsBase.__init__(self: UnknownType, document: str, certifications: Certifications, jinja_env: Environment, template_name: str, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize certification renderer.

---
## `ResumeRenderExecutiveSummaryBase` class

Base class for rendering resume executive summary section.

This class handles rendering of executive summary based on experience data.

Args:
    document (str): The text document to be rendered.
    experience (Experience): The experience data to be used for generating the summary.
    settings (ResumeExecutiveSummarySettings): The rendering settings for the executive summary.

Attributes:
    experience (Experience): The experience data to be used for generating the summary.
    document (str): The text document to be rendered.
    settings (ResumeExecutiveSummarySettings): The rendering settings for the executive summary.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.

Notes:
    1. Validates that experience is an instance of Experience.
    2. Validates that settings is an instance of ResumeExecutiveSummarySettings.
    3. Calls the superclass constructor to initialize common attributes.
    4. Assigns the provided experience and settings to instance attributes.

---
## method: `ResumeRenderExecutiveSummaryBase.__init__(self: UnknownType, document: str, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize the executive summary section.

---
## `ResumeRenderSkillsMatrixBase` class

Base class for rendering resume skills matrix section.

This class handles rendering of skills matrix based on experience data.

Args:
    document (str): The text document to be rendered.
    experience (Experience): The experience data to be used for generating the skills matrix.
    settings (ResumeSkillsMatrixSettings): The rendering settings for the skills matrix.

Attributes:
    experience (Experience): The experience data to be used for generating the skills matrix.
    document (str): The text document to be rendered.
    settings (ResumeSkillsMatrixSettings): The rendering settings for the skills matrix.
    errors (list[str]): List of errors encountered during rendering.
    warnings (list[str]): List of warnings encountered during rendering.

Notes:
    1. Validates that experience is an instance of Experience.
    2. Validates that settings is an instance of ResumeSkillsMatrixSettings.
    3. Calls the superclass constructor to initialize common attributes.
    4. Assigns the provided experience and settings to instance attributes.

---
## method: `ResumeRenderSkillsMatrixBase.__init__(self: UnknownType, document: str, experience: Experience, settings: ResumeSkillsMatrixSettings) -> None`

Initialize the skills matrix section.

---

===

===
# File: `__init__.py`

## function: `render_resume(resume: Resume, output_file: str) -> None`

Render a resume object to plain text format and save it to a file.

Args:
    resume (Resume): The resume object containing all resume data.
    output_file (str): The path to the output file where the plain text resume will be saved.

Returns:
    None: This function does not return a value.

Notes:
    1. The function retrieves the resume data from the Resume object.
    2. It formats the resume data into plain text, using appropriate indentation and spacing.
    3. The formatted text is written to the specified output file.
    4. The function performs disk access to write the plain text content to the output file.

---


===

===
# File: `executive_summary_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document (docx.document.Document): The Word document object to render the section into.
    experience (Experience): The experience data to be rendered.
    settings (ResumeExecutiveSummarySettings): Configuration settings for rendering the executive summary.

Returns:
    None

Notes:
    1. Set up the base class with the provided document, experience, and settings.
    2. Log the initialization process for debugging.

---

## function: `render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Validate that the experience has at least one role; raise ValueError if not.
    2. Create an ExecutiveSummary instance using the experience data.
    3. Generate the executive summary using the specified categories from settings.
    4. For each category in the summary:
        a. Add a heading with level 4 to the document.
        b. For each summary entry in the category:
            i. Add a new paragraph with the bullet point style.
            ii. Add the summary text as a run in the paragraph.
            iii. If no company is available, log a warning.
            iv. Otherwise, format the company and date:
                - If a last_date is present, format it as YYYY.
                - Otherwise, use "Present".
            v. Add the company and date as italicized text to the paragraph.
    5. No disk or network access occurs during this function.

---

## `RenderExecutiveSummarySection` class

Render experience for a functional resume.

---
## method: `RenderExecutiveSummarySection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document (docx.document.Document): The Word document object to render the section into.
    experience (Experience): The experience data to be rendered.
    settings (ResumeExecutiveSummarySettings): Configuration settings for rendering the executive summary.

Returns:
    None

Notes:
    1. Set up the base class with the provided document, experience, and settings.
    2. Log the initialization process for debugging.

---
## method: `RenderExecutiveSummarySection.render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Validate that the experience has at least one role; raise ValueError if not.
    2. Create an ExecutiveSummary instance using the experience data.
    3. Generate the executive summary using the specified categories from settings.
    4. For each category in the summary:
        a. Add a heading with level 4 to the document.
        b. For each summary entry in the category:
            i. Add a new paragraph with the bullet point style.
            ii. Add the summary text as a run in the paragraph.
            iii. If no company is available, log a warning.
            iv. Otherwise, format the company and date:
                - If a last_date is present, format it as YYYY.
                - Otherwise, use "Present".
            v. Add the company and date as italicized text to the paragraph.
    5. No disk or network access occurs during this function.

---

===

===
# File: `personal_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Parameters
----------
document : docx.document.Document
    The Word document object to which the personal section will be added.
personal : Personal
    The personal information object containing contact details, banner, note, websites, and visa status.
settings : ResumePersonalSettings
    The settings object that controls which elements of the personal section are rendered.

Notes
-----
1. Initialize the base class with the provided document, personal data, and settings.
2. Log a debug message indicating initialization is complete.

---

## function: `_contact_info(self: UnknownType) -> None`

Render the contact information section of the resume.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Extract the contact information from the personal attribute.
3. If a name is present in both the contact info and settings, add it as a heading.
4. Determine which contact details to render based on the settings.
5. If any contact details are to be rendered, add a new paragraph to the document.
6. If the email is to be rendered, add it as a hyperlink to the paragraph.
7. If the phone number is to be rendered, add it to the paragraph.
8. If the location is to be rendered, add it to the paragraph.

Returns
-------
None
    The method modifies the document in-place.

---

## function: `_banner(self: UnknownType) -> None`

Render the banner section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Retrieve the banner text from the personal object.
3. If the banner text is not empty, add a heading and the banner text to the document.

Returns
-------
None
    The method modifies the document in-place.

---

## function: `_note(self: UnknownType) -> None`

Render the note section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Retrieve the note text from the personal object.
3. If the note text is not empty, add a heading and the note text to the document.

Returns
-------
None
    The method modifies the document in-place.

---

## function: `_websites(self: UnknownType) -> str | None`

Render the websites section of a resume.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating that the websites section is being rendered.
2. Retrieve the user's websites from the personal object.
3. Initialize an empty string for the paragraph text and a new paragraph object.
4. Check if the user's GitHub profile is provided and if the GitHub setting is enabled. If so, add a hyperlink to the GitHub profile to the paragraph and set the has_content flag to True.
5. Repeat step 4 for the LinkedIn, website, and Twitter profiles.
6. If the paragraph has content, set its alignment to center.

Returns
-------
None
    The method modifies the document in-place.

---

## function: `_visa_status(self: UnknownType) -> None`

Render the visa status section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Create a new paragraph and set its alignment to center.
2. Retrieve the visa status object from the personal data.
3. If work authorization is enabled and present, add it to the paragraph.
4. If sponsorship requirement is enabled, determine if the value is "Yes" or "No" and add the appropriate text.
5. If both work authorization and sponsorship are present, add a separator "|".

Returns
-------
None
    The method modifies the document in-place.

---

## function: `render(self: UnknownType) -> None`

Render the personal section of a document.

Parameters
----------
self : object
    The instance of the class containing the personal information.

Notes
-----
1. Log a debug message indicating the start of personal section rendering.
2. Initialize an empty list for banner lines.
3. Add contact information to the document if enabled in settings.
4. Add websites to the document if enabled in settings.
5. Append banner text to banner lines if enabled in settings and not empty.
6. Append note text to banner lines if enabled in settings and not empty.
7. Add banner lines to the document if any exist.
8. Add visa status to the document if enabled in settings.

Returns
-------
None
    The method modifies the document in-place.

---

## `RenderPersonalSection` class

Render personal contact info section.

---
## method: `RenderPersonalSection.__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Parameters
----------
document : docx.document.Document
    The Word document object to which the personal section will be added.
personal : Personal
    The personal information object containing contact details, banner, note, websites, and visa status.
settings : ResumePersonalSettings
    The settings object that controls which elements of the personal section are rendered.

Notes
-----
1. Initialize the base class with the provided document, personal data, and settings.
2. Log a debug message indicating initialization is complete.

---
## method: `RenderPersonalSection._contact_info(self: UnknownType) -> None`

Render the contact information section of the resume.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Extract the contact information from the personal attribute.
3. If a name is present in both the contact info and settings, add it as a heading.
4. Determine which contact details to render based on the settings.
5. If any contact details are to be rendered, add a new paragraph to the document.
6. If the email is to be rendered, add it as a hyperlink to the paragraph.
7. If the phone number is to be rendered, add it to the paragraph.
8. If the location is to be rendered, add it to the paragraph.

Returns
-------
None
    The method modifies the document in-place.

---
## method: `RenderPersonalSection._banner(self: UnknownType) -> None`

Render the banner section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Retrieve the banner text from the personal object.
3. If the banner text is not empty, add a heading and the banner text to the document.

Returns
-------
None
    The method modifies the document in-place.

---
## method: `RenderPersonalSection._note(self: UnknownType) -> None`

Render the note section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating the section being rendered.
2. Retrieve the note text from the personal object.
3. If the note text is not empty, add a heading and the note text to the document.

Returns
-------
None
    The method modifies the document in-place.

---
## method: `RenderPersonalSection._websites(self: UnknownType) -> str | None`

Render the websites section of a resume.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Log a debug message indicating that the websites section is being rendered.
2. Retrieve the user's websites from the personal object.
3. Initialize an empty string for the paragraph text and a new paragraph object.
4. Check if the user's GitHub profile is provided and if the GitHub setting is enabled. If so, add a hyperlink to the GitHub profile to the paragraph and set the has_content flag to True.
5. Repeat step 4 for the LinkedIn, website, and Twitter profiles.
6. If the paragraph has content, set its alignment to center.

Returns
-------
None
    The method modifies the document in-place.

---
## method: `RenderPersonalSection._visa_status(self: UnknownType) -> None`

Render the visa status section.

Parameters
----------
self : object
    The instance of the class containing the personal and settings attributes.

Notes
-----
1. Create a new paragraph and set its alignment to center.
2. Retrieve the visa status object from the personal data.
3. If work authorization is enabled and present, add it to the paragraph.
4. If sponsorship requirement is enabled, determine if the value is "Yes" or "No" and add the appropriate text.
5. If both work authorization and sponsorship are present, add a separator "|".

Returns
-------
None
    The method modifies the document in-place.

---
## method: `RenderPersonalSection.render(self: UnknownType) -> None`

Render the personal section of a document.

Parameters
----------
self : object
    The instance of the class containing the personal information.

Notes
-----
1. Log a debug message indicating the start of personal section rendering.
2. Initialize an empty list for banner lines.
3. Add contact information to the document if enabled in settings.
4. Add websites to the document if enabled in settings.
5. Append banner text to banner lines if enabled in settings and not empty.
6. Append note text to banner lines if enabled in settings and not empty.
7. Add banner lines to the document if any exist.
8. Add visa status to the document if enabled in settings.

Returns
-------
None
    The method modifies the document in-place.

---

===

===
# File: `resume_main.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document (docx.document.Document): The Word document object to render into.
    resume (Resume): The parsed resume data structure containing personal, education, experience, certifications, and other sections.
    settings (ResumeRenderSettings): Configuration settings for rendering, including which sections to render and their formatting options.

Returns:
    None

Notes:
    1. Stores the provided document, resume, and settings as instance attributes.
    2. Initializes the base class ResumeRenderBase with the provided document, resume, and settings.
    3. No external disk, network, or database access occurs during initialization.

---

## function: `render(self: UnknownType) -> None`

Render the resume by sequentially rendering each enabled section.

Args:
    None

Returns:
    None

Notes:
    1. If personal information is present in the resume and personal section rendering is enabled, render the personal section.
    2. If certifications are present and certification section rendering is enabled, render the certifications section.
    3. If education data exists and education section rendering is enabled, render the education section.
    4. If experience data exists and executive summary rendering is enabled, add a centered heading "Executive Summary", then render the executive summary section using experience data.
    5. If experience data exists and skills matrix rendering is enabled (but not necessarily executive summary), render the skills matrix section using experience data.
    6. If both experience and executive summary rendering are enabled, insert a page break after the executive summary.
    7. If experience data exists and experience section rendering is enabled, render the full experience section.
    8. No external disk, network, or database access occurs during rendering.

---

## `RenderResume` class

Render a resume in basic format.

---
## method: `RenderResume.__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document (docx.document.Document): The Word document object to render into.
    resume (Resume): The parsed resume data structure containing personal, education, experience, certifications, and other sections.
    settings (ResumeRenderSettings): Configuration settings for rendering, including which sections to render and their formatting options.

Returns:
    None

Notes:
    1. Stores the provided document, resume, and settings as instance attributes.
    2. Initializes the base class ResumeRenderBase with the provided document, resume, and settings.
    3. No external disk, network, or database access occurs during initialization.

---
## method: `RenderResume.render(self: UnknownType) -> None`

Render the resume by sequentially rendering each enabled section.

Args:
    None

Returns:
    None

Notes:
    1. If personal information is present in the resume and personal section rendering is enabled, render the personal section.
    2. If certifications are present and certification section rendering is enabled, render the certifications section.
    3. If education data exists and education section rendering is enabled, render the education section.
    4. If experience data exists and executive summary rendering is enabled, add a centered heading "Executive Summary", then render the executive summary section using experience data.
    5. If experience data exists and skills matrix rendering is enabled (but not necessarily executive summary), render the skills matrix section using experience data.
    6. If both experience and executive summary rendering are enabled, insert a page break after the executive summary.
    7. If experience data exists and experience section rendering is enabled, render the full experience section.
    8. No external disk, network, or database access occurs during rendering.

---

===

===
# File: `skills_matrix_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> None`

Initialize skills render object.

Args:
    document: The DOCX document object to render the skills matrix into.
    experience: The experience data containing roles and skill information.
    settings: Configuration settings for rendering the skills matrix.
    parse_context: The context used for parsing input data (e.g., from resume text).

Returns:
    None

Notes:
    1. Validate that the parse_context is an instance of ParseContext.
    2. Store the parse_context for later use during rendering.
    3. Call the parent class's constructor to initialize shared functionality.

---

## function: `render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object has any roles. Raise a ValueError if not.
    2. Create a SkillsMatrix instance from the experience's roles.
    3. If the settings specify all_skills, generate a matrix for all skills using "*" as the skill name.
    4. Otherwise, generate a matrix for the skills specified in settings.skills.
    5. Calculate the number of table rows needed to display the skills (two skills per row).
    6. Add a table with the calculated rows and 4 columns, using the "Table Grid" style.
    7. Add a header row with bolded labels for "Skill" and "YOE (from - to)" in alternating columns.
    8. Iterate through the sorted skills and their data:
        a. Determine the correct row and column index for placement.
        b. Insert the skill name into the first column of the row.
        c. Align the skill text vertically in the center.
        d. Format the YOE string as "X years (from - to)" using first_used and last_used dates.
        e. Insert the formatted YOE string into the second column.
    9. Enable automatic table fitting to adjust column widths.
    10. No disk or network access is performed during this function.

---

## `RenderSkillsMatrixSection` class

Render skills for a functional resume.

---
## method: `RenderSkillsMatrixSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> None`

Initialize skills render object.

Args:
    document: The DOCX document object to render the skills matrix into.
    experience: The experience data containing roles and skill information.
    settings: Configuration settings for rendering the skills matrix.
    parse_context: The context used for parsing input data (e.g., from resume text).

Returns:
    None

Notes:
    1. Validate that the parse_context is an instance of ParseContext.
    2. Store the parse_context for later use during rendering.
    3. Call the parent class's constructor to initialize shared functionality.

---
## method: `RenderSkillsMatrixSection.render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object has any roles. Raise a ValueError if not.
    2. Create a SkillsMatrix instance from the experience's roles.
    3. If the settings specify all_skills, generate a matrix for all skills using "*" as the skill name.
    4. Otherwise, generate a matrix for the skills specified in settings.skills.
    5. Calculate the number of table rows needed to display the skills (two skills per row).
    6. Add a table with the calculated rows and 4 columns, using the "Table Grid" style.
    7. Add a header row with bolded labels for "Skill" and "YOE (from - to)" in alternating columns.
    8. Iterate through the sorted skills and their data:
        a. Determine the correct row and column index for placement.
        b. Insert the skill name into the first column of the row.
        c. Align the skill text vertically in the center.
        d. Format the YOE string as "X years (from - to)" using first_used and last_used dates.
        e. Insert the formatted YOE string into the second column.
    9. Enable automatic table fitting to adjust column widths.
    10. No disk or network access is performed during this function.

---

===

===
# File: `certifications_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document: The Word document object to render into.
    certification: The certification data to render.
    settings: The rendering settings for the certification section.

Notes:
    1. Initializes the parent class with the provided document, certification, and settings.

---

## function: `render(self: UnknownType) -> None`

Render the certification section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve the certification data from the instance.
    2. Create a new paragraph in the document with no space after it.
    3. Add a right-aligned tab stop at 7.4 inches.
    4. If the certification name exists and the name setting is enabled:
       a. Add a bold run with the certification name.
    5. If the issuer exists and the issuer setting is enabled:
       a. Add a tab character if the name was previously added.
       b. Add a run with the issuer name.
    6. If the issued date exists and the issued setting is enabled:
       a. Add a newline if a previous field (name or issuer) was added.
       b. Format the issued date as "Month YYYY".
       c. Add a run with "Issued: " followed by the formatted date.
    7. If the expiration date exists and the expires setting is enabled:
       a. Add a " - " separator if the issued date was added.
       b. Format the expiration date as "Month YYYY".
       c. Add a run with "Expires: " followed by the formatted date.
    8. This function modifies the document in-place and does not write to disk.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The Word document object to render into.
    certifications: A list of certification data to render.
    settings: The rendering settings for the certifications section.

Notes:
    1. Initializes the parent class with the provided document, certifications, and settings.

---

## function: `render(self: UnknownType) -> None`

Render the certifications section of a document.

Args:
    None

Returns:
    None

Notes:
    1. Log the start of the certifications section rendering.
    2. If there are no certifications, return early without adding anything.
    3. Add a level-2 heading titled "Certifications".
    4. For each certification in the list:
       a. Create a new RenderCertificationSection instance.
       b. Call the render method on that instance to add the certification to the document.
    5. This function modifies the document in-place and does not write to disk.

---

## `RenderCertificationSection` class

Render Certification Section.

---
## method: `RenderCertificationSection.__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document: The Word document object to render into.
    certification: The certification data to render.
    settings: The rendering settings for the certification section.

Notes:
    1. Initializes the parent class with the provided document, certification, and settings.

---
## method: `RenderCertificationSection.render(self: UnknownType) -> None`

Render the certification section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve the certification data from the instance.
    2. Create a new paragraph in the document with no space after it.
    3. Add a right-aligned tab stop at 7.4 inches.
    4. If the certification name exists and the name setting is enabled:
       a. Add a bold run with the certification name.
    5. If the issuer exists and the issuer setting is enabled:
       a. Add a tab character if the name was previously added.
       b. Add a run with the issuer name.
    6. If the issued date exists and the issued setting is enabled:
       a. Add a newline if a previous field (name or issuer) was added.
       b. Format the issued date as "Month YYYY".
       c. Add a run with "Issued: " followed by the formatted date.
    7. If the expiration date exists and the expires setting is enabled:
       a. Add a " - " separator if the issued date was added.
       b. Format the expiration date as "Month YYYY".
       c. Add a run with "Expires: " followed by the formatted date.
    8. This function modifies the document in-place and does not write to disk.

---
## `RenderCertificationsSection` class

Render Certifications Section.

---
## method: `RenderCertificationsSection.__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The Word document object to render into.
    certifications: A list of certification data to render.
    settings: The rendering settings for the certifications section.

Notes:
    1. Initializes the parent class with the provided document, certifications, and settings.

---
## method: `RenderCertificationsSection.render(self: UnknownType) -> None`

Render the certifications section of a document.

Args:
    None

Returns:
    None

Notes:
    1. Log the start of the certifications section rendering.
    2. If there are no certifications, return early without adding anything.
    3. Add a level-2 heading titled "Certifications".
    4. For each certification in the list:
       a. Create a new RenderCertificationSection instance.
       b. Call the render method on that instance to add the certification to the document.
    5. This function modifies the document in-place and does not write to disk.

---

===

===
# File: `education_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

Args:
    document: The DOCX document to render into.
    degree: The degree to render.
    settings: The rendering settings for degrees.

Returns:
    None

Notes:
    1. Calls the parent constructor with the provided document, degree, and settings.

---

## function: `render(self: UnknownType) -> None`

Render a single degree.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of degree rendering.
    2. Adds a new paragraph to the document.
    3. Sets a right-aligned tab stop at 7.4 inches.
    4. If the school name is provided and enabled in settings, adds it in bold with increased font size.
    5. If the degree name is provided and enabled in settings, adds it after a tab, in bold, and adds a line break.
    6. If the start date is provided and enabled in settings, formats and adds it to the paragraph.
    7. If the end date is provided and enabled in settings, formats and adds it to the paragraph with a dash.
    8. If the GPA is provided and enabled in settings, adds it after a tab.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

Args:
    document: The DOCX document to render into.
    education: The education data to render.
    settings: The rendering settings for education.

Returns:
    None

Notes:
    1. Calls the parent constructor with the provided document, education, and settings.

---

## function: `render(self: UnknownType) -> None`

Render the education section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of education rendering.
    2. If degree rendering is disabled in settings, exits early.
    3. Adds a centered heading titled "Education" with level 2.
    4. Iterates through each degree in the education.
    5. For each degree, creates a RenderDegreeSection instance and calls its render method.
    6. Adds a blank paragraph between degrees.

---

## `RenderDegreeSection` class

Render Degree Section.

---
## method: `RenderDegreeSection.__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

Args:
    document: The DOCX document to render into.
    degree: The degree to render.
    settings: The rendering settings for degrees.

Returns:
    None

Notes:
    1. Calls the parent constructor with the provided document, degree, and settings.

---
## method: `RenderDegreeSection.render(self: UnknownType) -> None`

Render a single degree.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of degree rendering.
    2. Adds a new paragraph to the document.
    3. Sets a right-aligned tab stop at 7.4 inches.
    4. If the school name is provided and enabled in settings, adds it in bold with increased font size.
    5. If the degree name is provided and enabled in settings, adds it after a tab, in bold, and adds a line break.
    6. If the start date is provided and enabled in settings, formats and adds it to the paragraph.
    7. If the end date is provided and enabled in settings, formats and adds it to the paragraph with a dash.
    8. If the GPA is provided and enabled in settings, adds it after a tab.

---
## `RenderEducationSection` class

Render Education Section.

---
## method: `RenderEducationSection.__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

Args:
    document: The DOCX document to render into.
    education: The education data to render.
    settings: The rendering settings for education.

Returns:
    None

Notes:
    1. Calls the parent constructor with the provided document, education, and settings.

---
## method: `RenderEducationSection.render(self: UnknownType) -> None`

Render the education section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of education rendering.
    2. If degree rendering is disabled in settings, exits early.
    3. Adds a centered heading titled "Education" with level 2.
    4. Iterates through each degree in the education.
    5. For each degree, creates a RenderDegreeSection instance and calls its render method.
    6. Adds a blank paragraph between degrees.

---

===

===
# File: `experience_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The DOCX document object to render into.
    role: The role data to render.
    settings: The rendering settings for roles.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, role, and settings.
    2. Logs a debug message indicating initialization has started.

---

## function: `_skills(self: UnknownType) -> list[str]`

Render role skills section.

Args:
    None

Returns:
    A list containing strings of skills. The list is empty if no skills are present.

Notes:
    1. Creates a new paragraph in the document.
    2. Checks if skills are present in the role and if the settings allow displaying skills.
    3. If skills are present, joins them with commas and adds them as italicized text.
    4. Sets the font size to be two points smaller than the base font size.
    5. Logs a debug message about the skills rendering process.

---

## function: `_details(self: UnknownType) -> list[str]`

Render role details section.

Args:
    None

Returns:
    A list of strings containing details like job category, location, agency name, and employment type.

Notes:
    1. Initializes an empty list to store the details.
    2. Checks if job category is present and if it should be displayed.
    3. Adds job category to the list if applicable.
    4. Checks if location is present and if it should be displayed.
    5. Adds location to the list if applicable.
    6. Checks if agency name is present and if it should be displayed.
    7. Adds agency name to the list if applicable.
    8. Checks if employment type is present and if it should be displayed.
    9. Adds employment type to the list if applicable.
    10. Returns the list of details.

---

## function: `_title_and_company(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> None`

Render role title and company section.

Args:
    paragraph: The paragraph object to add the title and company to.

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of title and company rendering.
    2. Retrieves the basics information from the role.
    3. Checks if the title is present; if not, raises a ValueError with an error message.
    4. Adds the title as bold and underlined text to the paragraph.
    5. Sets the font size to be two points larger than the base font size.
    6. Checks if the company name is present; if not, raises a ValueError with an error message.
    7. Adds the company name with a tab character and bold formatting to the paragraph.
    8. Sets the font size to be two points larger than the base font size.

---

## function: `_dates_and_location(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> list[str]`

Render role dates section.

Args:
    paragraph: The paragraph object to add the dates and location to.

Returns:
    A list of strings containing the formatted date and location information.

Notes:
    1. Logs a debug message indicating the start of date and location rendering.
    2. Retrieves the basics information from the role.
    3. Creates a new run object for the date information.
    4. Checks if the start date is present; if not, logs a warning message.
    5. Formats the start date as "Month Year" and adds it to the run.
    6. If an end date is present, formats it as "Month Year" and adds it to the run with a hyphen.
    7. If no end date is present, adds "Present" to the run.
    8. If location is present and should be displayed, adds it to the paragraph with a tab.
    9. Returns the list of formatted date and location strings.

---

## function: `_render_task(self: UnknownType, paragraph: docx.text.paragraph.Paragraph, task_line: str) -> None`

Render a single task line with skill highlighting.

Args:
    paragraph: The paragraph object to add the task to.
    task_line: The task text to render.

Returns:
    None

Notes:
    1. Checks if skills are present and if the settings allow including tasks.
    2. Splits the task line using the skills splitter function.
    3. Initializes leading and trailing space flags.
    4. Iterates through each fragment in the task line.
    5. Creates a new run for each fragment.
    6. Determines if a trailing space is needed based on punctuation.
    7. If the fragment is a skill, adds it in bold.
    8. Adds leading space if needed.
    9. Adds the fragment text to the run.
    10. Adds trailing space if needed.
    11. Adds a line break after the last fragment.

---

## function: `_responsibilities(self: UnknownType) -> None`

Render role responsibilities section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of responsibilities rendering.
    2. Creates two paragraphs: one for situation and one for tasks.
    3. Sets spacing before and after both paragraphs.
    4. Splits the responsibilities text by double newlines and then by single newlines.
    5. Iterates through each line in the responsibilities.
    6. If the line starts with "* ", renders it as a task if tasks are included.
    7. If the line doesn't start with "* ", adds it to the situation paragraph if situation is included.
    8. Adds line breaks as needed.

---

## function: `_description(self: UnknownType) -> None`

Render role summary and details section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if a summary is present and if the settings allow displaying it.
    2. If a summary is present, creates a new paragraph and adds the summary text in bold and italic.
    3. Sets the spacing after the paragraph.
    4. Sets the spacing before the paragraph.
    5. Checks if responsibilities are present and if the settings allow displaying them.
    6. If responsibilities are present, calls the responsibilities rendering method.

---

## function: `render(self: UnknownType) -> None`

Render role overview/basics section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Creates a paragraph for basics information.
    3. Sets spacing after the paragraph.
    4. Renders the title and company information.
    5. Adds tab stops to the basics paragraph for formatting.
    6. Creates a paragraph for dates and location.
    7. Adds tab stops to the dates paragraph for formatting.
    8. Renders the dates and location information.
    9. Sets spacing after the dates paragraph.
    10. Renders the description section.
    11. Renders the skills section.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The DOCX document object to render into.
    roles: The list of role data to render.
    settings: The rendering settings for roles.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, roles, and settings.
    2. Logs a debug message indicating initialization has started.

---

## function: `render(self: UnknownType) -> None`

Render roles section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Checks if there are any roles to render.
    3. If roles exist, adds a centered heading with the text "Work History".
    4. If no roles exist, logs an info message.
    5. Iterates through each role and renders it using the RenderRoleSection class.
    6. Adds a blank paragraph after each role with 12 points of spacing after.
    7. Adds a horizontal line after each role.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The DOCX document object to render into.
    project: The project data to render.
    settings: The rendering settings for projects.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, project, and settings.
    2. Logs a debug message indicating initialization has started.

---

## function: `_overview(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> None`

Render project overview section.

Args:
    paragraph: The paragraph object to add the overview to.

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of overview rendering.
    2. Retrieves the overview information from the project.
    3. Adds the project title as bold text to the paragraph.
    4. Adds a tab character to the paragraph.
    5. Sets spacing after the paragraph.
    6. Adds a hyperlink to the project website using the add_hyperlink function.

---

## function: `_skills(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> list[str]`

Render project skills section.

Args:
    paragraph: The paragraph object to add the skills to.

Returns:
    A list of strings containing the project skills.

Notes:
    1. Logs a debug message indicating the start of skills rendering.
    2. Joins the project skills with commas.
    3. Creates a new run object for the skills text.
    4. Adds the skills text with "Skills: " prefix.
    5. Sets the text to be italic.
    6. Returns the list of skills.

---

## function: `render(self: UnknownType) -> None`

Render project section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of project rendering.
    2. Creates a paragraph for the project information.
    3. Adds tab stops to the paragraph for formatting.
    4. Checks if the overview should be displayed and if it exists.
    5. If the overview should be displayed, renders the overview section.
    6. Sets spacing after the overview paragraph.
    7. Checks if the description should be displayed and if it exists.
    8. If the description should be displayed, adds each line of the description as a separate run with line breaks.
    9. Sets spacing before and after the description paragraph.
    10. Checks if skills should be displayed and if they exist.
    11. If skills should be displayed, adds a new paragraph for skills and renders them.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The DOCX document object to render into.
    projects: The list of project data to render.
    settings: The rendering settings for projects.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, projects, and settings.
    2. Logs a debug message indicating initialization has started.

---

## function: `render(self: UnknownType) -> None`

Render projects section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of projects rendering.
    2. Checks if there are any projects to render.
    3. If projects exist, adds a heading with the text "Projects".
    4. Iterates through each project and renders it using the RenderProjectSection class.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The DOCX document object to render into.
    experience: The experience data to render.
    settings: The rendering settings for experience.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, experience, and settings.
    2. Logs a debug message indicating initialization has started.

---

## function: `render(self: UnknownType) -> None`

Render experience section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of experience rendering.
    2. Checks if roles should be rendered and if they exist.
    3. If roles should be rendered and they exist, creates a roles section with the appropriate settings.
    4. Checks if projects should be rendered and if they exist.
    5. If projects should be rendered and they exist, creates a projects section with the appropriate settings.

---

## `RenderRoleSection` class

Render experience roles section.

---
## method: `RenderRoleSection.__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The DOCX document object to render into.
    role: The role data to render.
    settings: The rendering settings for roles.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, role, and settings.
    2. Logs a debug message indicating initialization has started.

---
## method: `RenderRoleSection._skills(self: UnknownType) -> list[str]`

Render role skills section.

Args:
    None

Returns:
    A list containing strings of skills. The list is empty if no skills are present.

Notes:
    1. Creates a new paragraph in the document.
    2. Checks if skills are present in the role and if the settings allow displaying skills.
    3. If skills are present, joins them with commas and adds them as italicized text.
    4. Sets the font size to be two points smaller than the base font size.
    5. Logs a debug message about the skills rendering process.

---
## method: `RenderRoleSection._details(self: UnknownType) -> list[str]`

Render role details section.

Args:
    None

Returns:
    A list of strings containing details like job category, location, agency name, and employment type.

Notes:
    1. Initializes an empty list to store the details.
    2. Checks if job category is present and if it should be displayed.
    3. Adds job category to the list if applicable.
    4. Checks if location is present and if it should be displayed.
    5. Adds location to the list if applicable.
    6. Checks if agency name is present and if it should be displayed.
    7. Adds agency name to the list if applicable.
    8. Checks if employment type is present and if it should be displayed.
    9. Adds employment type to the list if applicable.
    10. Returns the list of details.

---
## method: `RenderRoleSection._title_and_company(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> None`

Render role title and company section.

Args:
    paragraph: The paragraph object to add the title and company to.

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of title and company rendering.
    2. Retrieves the basics information from the role.
    3. Checks if the title is present; if not, raises a ValueError with an error message.
    4. Adds the title as bold and underlined text to the paragraph.
    5. Sets the font size to be two points larger than the base font size.
    6. Checks if the company name is present; if not, raises a ValueError with an error message.
    7. Adds the company name with a tab character and bold formatting to the paragraph.
    8. Sets the font size to be two points larger than the base font size.

---
## method: `RenderRoleSection._dates_and_location(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> list[str]`

Render role dates section.

Args:
    paragraph: The paragraph object to add the dates and location to.

Returns:
    A list of strings containing the formatted date and location information.

Notes:
    1. Logs a debug message indicating the start of date and location rendering.
    2. Retrieves the basics information from the role.
    3. Creates a new run object for the date information.
    4. Checks if the start date is present; if not, logs a warning message.
    5. Formats the start date as "Month Year" and adds it to the run.
    6. If an end date is present, formats it as "Month Year" and adds it to the run with a hyphen.
    7. If no end date is present, adds "Present" to the run.
    8. If location is present and should be displayed, adds it to the paragraph with a tab.
    9. Returns the list of formatted date and location strings.

---
## method: `RenderRoleSection._render_task(self: UnknownType, paragraph: docx.text.paragraph.Paragraph, task_line: str) -> None`

Render a single task line with skill highlighting.

Args:
    paragraph: The paragraph object to add the task to.
    task_line: The task text to render.

Returns:
    None

Notes:
    1. Checks if skills are present and if the settings allow including tasks.
    2. Splits the task line using the skills splitter function.
    3. Initializes leading and trailing space flags.
    4. Iterates through each fragment in the task line.
    5. Creates a new run for each fragment.
    6. Determines if a trailing space is needed based on punctuation.
    7. If the fragment is a skill, adds it in bold.
    8. Adds leading space if needed.
    9. Adds the fragment text to the run.
    10. Adds trailing space if needed.
    11. Adds a line break after the last fragment.

---
## method: `RenderRoleSection._responsibilities(self: UnknownType) -> None`

Render role responsibilities section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of responsibilities rendering.
    2. Creates two paragraphs: one for situation and one for tasks.
    3. Sets spacing before and after both paragraphs.
    4. Splits the responsibilities text by double newlines and then by single newlines.
    5. Iterates through each line in the responsibilities.
    6. If the line starts with "* ", renders it as a task if tasks are included.
    7. If the line doesn't start with "* ", adds it to the situation paragraph if situation is included.
    8. Adds line breaks as needed.

---
## method: `RenderRoleSection._description(self: UnknownType) -> None`

Render role summary and details section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if a summary is present and if the settings allow displaying it.
    2. If a summary is present, creates a new paragraph and adds the summary text in bold and italic.
    3. Sets the spacing after the paragraph.
    4. Sets the spacing before the paragraph.
    5. Checks if responsibilities are present and if the settings allow displaying them.
    6. If responsibilities are present, calls the responsibilities rendering method.

---
## method: `RenderRoleSection.render(self: UnknownType) -> None`

Render role overview/basics section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Creates a paragraph for basics information.
    3. Sets spacing after the paragraph.
    4. Renders the title and company information.
    5. Adds tab stops to the basics paragraph for formatting.
    6. Creates a paragraph for dates and location.
    7. Adds tab stops to the dates paragraph for formatting.
    8. Renders the dates and location information.
    9. Sets spacing after the dates paragraph.
    10. Renders the description section.
    11. Renders the skills section.

---
## `RenderRolesSection` class

Render experience roles section.

---
## method: `RenderRolesSection.__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The DOCX document object to render into.
    roles: The list of role data to render.
    settings: The rendering settings for roles.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, roles, and settings.
    2. Logs a debug message indicating initialization has started.

---
## method: `RenderRolesSection.render(self: UnknownType) -> None`

Render roles section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Checks if there are any roles to render.
    3. If roles exist, adds a centered heading with the text "Work History".
    4. If no roles exist, logs an info message.
    5. Iterates through each role and renders it using the RenderRoleSection class.
    6. Adds a blank paragraph after each role with 12 points of spacing after.
    7. Adds a horizontal line after each role.

---
## `RenderProjectSection` class

Render experience project section.

---
## method: `RenderProjectSection.__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The DOCX document object to render into.
    project: The project data to render.
    settings: The rendering settings for projects.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, project, and settings.
    2. Logs a debug message indicating initialization has started.

---
## method: `RenderProjectSection._overview(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> None`

Render project overview section.

Args:
    paragraph: The paragraph object to add the overview to.

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of overview rendering.
    2. Retrieves the overview information from the project.
    3. Adds the project title as bold text to the paragraph.
    4. Adds a tab character to the paragraph.
    5. Sets spacing after the paragraph.
    6. Adds a hyperlink to the project website using the add_hyperlink function.

---
## method: `RenderProjectSection._skills(self: UnknownType, paragraph: docx.text.paragraph.Paragraph) -> list[str]`

Render project skills section.

Args:
    paragraph: The paragraph object to add the skills to.

Returns:
    A list of strings containing the project skills.

Notes:
    1. Logs a debug message indicating the start of skills rendering.
    2. Joins the project skills with commas.
    3. Creates a new run object for the skills text.
    4. Adds the skills text with "Skills: " prefix.
    5. Sets the text to be italic.
    6. Returns the list of skills.

---
## method: `RenderProjectSection.render(self: UnknownType) -> None`

Render project section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of project rendering.
    2. Creates a paragraph for the project information.
    3. Adds tab stops to the paragraph for formatting.
    4. Checks if the overview should be displayed and if it exists.
    5. If the overview should be displayed, renders the overview section.
    6. Sets spacing after the overview paragraph.
    7. Checks if the description should be displayed and if it exists.
    8. If the description should be displayed, adds each line of the description as a separate run with line breaks.
    9. Sets spacing before and after the description paragraph.
    10. Checks if skills should be displayed and if they exist.
    11. If skills should be displayed, adds a new paragraph for skills and renders them.

---
## `RenderProjectsSection` class

Render experience projects section.

---
## method: `RenderProjectsSection.__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The DOCX document object to render into.
    projects: The list of project data to render.
    settings: The rendering settings for projects.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, projects, and settings.
    2. Logs a debug message indicating initialization has started.

---
## method: `RenderProjectsSection.render(self: UnknownType) -> None`

Render projects section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of projects rendering.
    2. Checks if there are any projects to render.
    3. If projects exist, adds a heading with the text "Projects".
    4. Iterates through each project and renders it using the RenderProjectSection class.

---
## `RenderExperienceSection` class

Render experience section.

---
## method: `RenderExperienceSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The DOCX document object to render into.
    experience: The experience data to render.
    settings: The rendering settings for experience.

Returns:
    None

Notes:
    1. Initializes the base class with the provided document, experience, and settings.
    2. Logs a debug message indicating initialization has started.

---
## method: `RenderExperienceSection.render(self: UnknownType) -> None`

Render experience section.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of experience rendering.
    2. Checks if roles should be rendered and if they exist.
    3. If roles should be rendered and they exist, creates a roles section with the appropriate settings.
    4. Checks if projects should be rendered and if they exist.
    5. If projects should be rendered and they exist, creates a projects section with the appropriate settings.

---

===

===
# File: `__init__.py`


===

===
# File: `certifications_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document: The Word document object to which the certification will be added.
    certification: The Certification object containing details about the certification.
    settings: The settings object that determines which fields to include in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize base functionality.
    2. Stores the provided document, certification, and settings as instance attributes.

---

## function: `render(self: UnknownType) -> None`

Render the certification section.

Args:
    None

Returns:
    None

Notes:
    1. Initializes an empty list to hold the lines of text to be rendered.
    2. Checks if the certification name exists and the name setting is enabled, and adds it to the lines if so.
    3. Checks if the issuer exists and the issuer setting is enabled, and adds it to the lines if so.
    4. Checks if the issued date exists and the issued setting is enabled, formats it as "Month Year", and adds it to the lines if so.
    5. Checks if the expiration date exists and the expires setting is enabled, formats it as "Month Year", and adds it to the lines if so.
    6. If any lines were collected, joins them with newlines and adds a new paragraph to the document with the resulting text.
    7. No disk, network, or database access occurs during this method.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The Word document object to which the certifications will be added.
    certifications: A list of Certification objects to be rendered.
    settings: The settings object that determines which fields to include in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize base functionality.
    2. Stores the provided document, certifications, and settings as instance attributes.

---

## function: `render(self: UnknownType) -> None`

Render the certifications section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if there are any certifications to render.
    2. If certifications exist, adds a level-2 heading titled "Certifications" to the document.
    3. Iterates through each certification in the list.
    4. For each certification, creates a new RenderCertificationSection instance and calls its render method to add the certification details to the document.
    5. No disk, network, or database access occurs during this method.

---

## `RenderCertificationSection` class

Render Certification Section.

---
## method: `RenderCertificationSection.__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document: The Word document object to which the certification will be added.
    certification: The Certification object containing details about the certification.
    settings: The settings object that determines which fields to include in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize base functionality.
    2. Stores the provided document, certification, and settings as instance attributes.

---
## method: `RenderCertificationSection.render(self: UnknownType) -> None`

Render the certification section.

Args:
    None

Returns:
    None

Notes:
    1. Initializes an empty list to hold the lines of text to be rendered.
    2. Checks if the certification name exists and the name setting is enabled, and adds it to the lines if so.
    3. Checks if the issuer exists and the issuer setting is enabled, and adds it to the lines if so.
    4. Checks if the issued date exists and the issued setting is enabled, formats it as "Month Year", and adds it to the lines if so.
    5. Checks if the expiration date exists and the expires setting is enabled, formats it as "Month Year", and adds it to the lines if so.
    6. If any lines were collected, joins them with newlines and adds a new paragraph to the document with the resulting text.
    7. No disk, network, or database access occurs during this method.

---
## `RenderCertificationsSection` class

Render Certifications Section.

---
## method: `RenderCertificationsSection.__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The Word document object to which the certifications will be added.
    certifications: A list of Certification objects to be rendered.
    settings: The settings object that determines which fields to include in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize base functionality.
    2. Stores the provided document, certifications, and settings as instance attributes.

---
## method: `RenderCertificationsSection.render(self: UnknownType) -> None`

Render the certifications section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if there are any certifications to render.
    2. If certifications exist, adds a level-2 heading titled "Certifications" to the document.
    3. Iterates through each certification in the list.
    4. For each certification, creates a new RenderCertificationSection instance and calls its render method to add the certification details to the document.
    5. No disk, network, or database access occurs during this method.

---

===

===
# File: `experience_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to which the role content will be added.
    role: The Role object containing role-specific details such as company, title, dates, etc.
    settings: The settings object that controls which parts of the role to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, role, and settings.
    2. Log a debug message indicating initialization.

---

## function: `_skills(self: UnknownType) -> list[str]`

Render role skills section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for skills. If no skills are present or settings are disabled, returns an empty list.

Notes:
    1. Initialize an empty list to hold the skill lines.
    2. Check if the role has skills and if the skills setting is enabled.
    3. If both conditions are true, join the skills into a comma-separated string and append it to the list with the label "Skills: ".
    4. Return the list of skill lines.

---

## function: `_details(self: UnknownType) -> list[str]`

Render role details section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for role details such as job category, location, agency, or employment type. Returns an empty list if no details are to be rendered.

Notes:
    1. Initialize an empty list to store detail lines.
    2. Extract the role's basics information.
    3. Check if job category is present and if the job_category setting is enabled, then append the formatted line.
    4. Repeat for location, agency name, and employment type if applicable and settings are enabled.
    5. Return the list of detail lines.

---

## function: `_dates(self: UnknownType) -> list[str]`

Render role dates section.

Args:
    None.

Returns:
    A list of strings, with a single entry containing the formatted date range (e.g., "01-2020 - 12-2022" or "01-2020 - Present").

Notes:
    1. Initialize an empty list to hold date lines.
    2. Extract the role's basics information.
    3. Validate that a start date is present; if not, append a warning to errors and return.
    4. Format the start date as "MM-YYYY".
    5. If an end date is present, format it as "MM-YYYY" and append it with a hyphen.
    6. If no end date is present, append " - Present".
    7. Return the formatted date string as a list with one element.

---

## function: `render(self: UnknownType) -> None`

Render role overview/basics section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initialize an empty list to hold paragraph lines.
    2. Extract the role's basics information.
    3. Check if the company name is present; if not, append a warning and log it.
    4. Append the formatted "Company: <name>" line.
    5. Render the dates using _dates method and extend the paragraph lines.
    6. Check if the title is present; if not, append a warning and log it.
    7. Append the formatted "Title: <title>" line.
    8. Render the details using _details method and extend the paragraph lines.
    9. Clean the paragraph lines by replacing double newlines with single newlines.
    10. If any paragraph lines exist, add a paragraph to the document with the joined lines.
    11. If a summary exists and summary setting is enabled, add it as a paragraph.
    12. If responsibilities exist and responsibilities setting is enabled, add them as a paragraph with cleaned text.
    13. Render the skills using _skills method and add them as a paragraph if any exist.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to which the roles content will be added.
    roles: A list of Role objects representing job roles to be rendered.
    settings: The settings object that controls which parts of the roles to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, roles, and settings.

---

## function: `render(self: UnknownType) -> None`

Render roles section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. Store the roles list to avoid filtering twice.
    3. Add a heading "Work History" at level 2 if any roles exist.
    4. If no roles exist, log an info message and return.
    5. Iterate over each role in the roles list.
    6. For each role, create a RenderRoleSection instance and call its render method.
    7. After each role (except the last), add two blank paragraphs to separate entries.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The Docx document object to which the project content will be added.
    project: The Project object containing project details such as description, skills, URLs, etc.
    settings: The settings object that controls which parts of the project to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, project, and settings.
    2. Log a debug message indicating initialization.

---

## function: `_overview(self: UnknownType) -> list[str]`

Render project overview section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for the project overview such as URL description, URL, start date, or end date. Returns an empty list if no overview data is to be rendered.

Notes:
    1. Initialize an empty list to store overview lines.
    2. Extract the project's overview information.
    3. If URL description is enabled and present, format it as a string.
    4. If URL is enabled and present, add it in parentheses to the URL description line.
    5. Strip and add the resulting URL line if it is not empty.
    6. If start date is enabled and present, format the date as "Month Year" and add it.
    7. If end date is enabled and present, format the date as "Month Year" and add it.
    8. Return the list of overview lines.

---

## function: `_skills(self: UnknownType) -> list[str]`

Render project skills section.

Args:
    None.

Returns:
    A list of strings, with a single entry containing "Skills: <comma-separated skills>" if skills are present and enabled. Returns an empty list otherwise.

Notes:
    1. Initialize an empty list to store skill lines.
    2. Join the project's skills into a comma-separated string.
    3. Append a formatted "Skills: ..." line to the list.
    4. Return the list of skill lines.

---

## function: `render(self: UnknownType) -> None`

Render project section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. Initialize an empty list to store paragraph lines.
    3. If overview is enabled and the project has an overview, render it using _overview method and extend the paragraph lines.
    4. If description is enabled and the project has a description, append the description text.
    5. If skills are enabled and the project has skills, render them using _skills method and extend the paragraph lines.
    6. If any paragraph lines exist, add a paragraph to the document with the joined lines.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The Docx document object to which the projects content will be added.
    projects: A list of Project objects representing projects to be rendered.
    settings: The settings object that controls which parts of the projects to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, projects, and settings.
    2. Log a debug message indicating initialization.

---

## function: `render(self: UnknownType) -> None`

Render projects section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. If any projects exist, add a heading "Projects" at level 2.
    3. Iterate over each project in the projects list.
    4. For each project, create a RenderProjectSection instance and call its render method.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to which the experience content will be added.
    experience: The Experience object containing roles and projects to be rendered.
    settings: The settings object that controls which parts of experience to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, experience, and settings.
    2. Log a debug message indicating initialization.

---

## function: `render(self: UnknownType) -> None`

Render experience section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. If roles are enabled and the experience has roles, render them using RenderRolesSection.
    3. If projects are enabled and the experience has projects, render them using RenderProjectsSection.

---

## `RenderRoleSection` class

Render experience roles section.

---
## method: `RenderRoleSection.__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to which the role content will be added.
    role: The Role object containing role-specific details such as company, title, dates, etc.
    settings: The settings object that controls which parts of the role to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, role, and settings.
    2. Log a debug message indicating initialization.

---
## method: `RenderRoleSection._skills(self: UnknownType) -> list[str]`

Render role skills section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for skills. If no skills are present or settings are disabled, returns an empty list.

Notes:
    1. Initialize an empty list to hold the skill lines.
    2. Check if the role has skills and if the skills setting is enabled.
    3. If both conditions are true, join the skills into a comma-separated string and append it to the list with the label "Skills: ".
    4. Return the list of skill lines.

---
## method: `RenderRoleSection._details(self: UnknownType) -> list[str]`

Render role details section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for role details such as job category, location, agency, or employment type. Returns an empty list if no details are to be rendered.

Notes:
    1. Initialize an empty list to store detail lines.
    2. Extract the role's basics information.
    3. Check if job category is present and if the job_category setting is enabled, then append the formatted line.
    4. Repeat for location, agency name, and employment type if applicable and settings are enabled.
    5. Return the list of detail lines.

---
## method: `RenderRoleSection._dates(self: UnknownType) -> list[str]`

Render role dates section.

Args:
    None.

Returns:
    A list of strings, with a single entry containing the formatted date range (e.g., "01-2020 - 12-2022" or "01-2020 - Present").

Notes:
    1. Initialize an empty list to hold date lines.
    2. Extract the role's basics information.
    3. Validate that a start date is present; if not, append a warning to errors and return.
    4. Format the start date as "MM-YYYY".
    5. If an end date is present, format it as "MM-YYYY" and append it with a hyphen.
    6. If no end date is present, append " - Present".
    7. Return the formatted date string as a list with one element.

---
## method: `RenderRoleSection.render(self: UnknownType) -> None`

Render role overview/basics section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initialize an empty list to hold paragraph lines.
    2. Extract the role's basics information.
    3. Check if the company name is present; if not, append a warning and log it.
    4. Append the formatted "Company: <name>" line.
    5. Render the dates using _dates method and extend the paragraph lines.
    6. Check if the title is present; if not, append a warning and log it.
    7. Append the formatted "Title: <title>" line.
    8. Render the details using _details method and extend the paragraph lines.
    9. Clean the paragraph lines by replacing double newlines with single newlines.
    10. If any paragraph lines exist, add a paragraph to the document with the joined lines.
    11. If a summary exists and summary setting is enabled, add it as a paragraph.
    12. If responsibilities exist and responsibilities setting is enabled, add them as a paragraph with cleaned text.
    13. Render the skills using _skills method and add them as a paragraph if any exist.

---
## `RenderRolesSection` class

Render experience roles section.

---
## method: `RenderRolesSection.__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to which the roles content will be added.
    roles: A list of Role objects representing job roles to be rendered.
    settings: The settings object that controls which parts of the roles to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, roles, and settings.

---
## method: `RenderRolesSection.render(self: UnknownType) -> None`

Render roles section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. Store the roles list to avoid filtering twice.
    3. Add a heading "Work History" at level 2 if any roles exist.
    4. If no roles exist, log an info message and return.
    5. Iterate over each role in the roles list.
    6. For each role, create a RenderRoleSection instance and call its render method.
    7. After each role (except the last), add two blank paragraphs to separate entries.

---
## `RenderProjectSection` class

Render experience project section.

---
## method: `RenderProjectSection.__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The Docx document object to which the project content will be added.
    project: The Project object containing project details such as description, skills, URLs, etc.
    settings: The settings object that controls which parts of the project to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, project, and settings.
    2. Log a debug message indicating initialization.

---
## method: `RenderProjectSection._overview(self: UnknownType) -> list[str]`

Render project overview section.

Args:
    None.

Returns:
    A list of strings, each representing a formatted line for the project overview such as URL description, URL, start date, or end date. Returns an empty list if no overview data is to be rendered.

Notes:
    1. Initialize an empty list to store overview lines.
    2. Extract the project's overview information.
    3. If URL description is enabled and present, format it as a string.
    4. If URL is enabled and present, add it in parentheses to the URL description line.
    5. Strip and add the resulting URL line if it is not empty.
    6. If start date is enabled and present, format the date as "Month Year" and add it.
    7. If end date is enabled and present, format the date as "Month Year" and add it.
    8. Return the list of overview lines.

---
## method: `RenderProjectSection._skills(self: UnknownType) -> list[str]`

Render project skills section.

Args:
    None.

Returns:
    A list of strings, with a single entry containing "Skills: <comma-separated skills>" if skills are present and enabled. Returns an empty list otherwise.

Notes:
    1. Initialize an empty list to store skill lines.
    2. Join the project's skills into a comma-separated string.
    3. Append a formatted "Skills: ..." line to the list.
    4. Return the list of skill lines.

---
## method: `RenderProjectSection.render(self: UnknownType) -> None`

Render project section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. Initialize an empty list to store paragraph lines.
    3. If overview is enabled and the project has an overview, render it using _overview method and extend the paragraph lines.
    4. If description is enabled and the project has a description, append the description text.
    5. If skills are enabled and the project has skills, render them using _skills method and extend the paragraph lines.
    6. If any paragraph lines exist, add a paragraph to the document with the joined lines.

---
## `RenderProjectsSection` class

Render experience projects section.

---
## method: `RenderProjectsSection.__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The Docx document object to which the projects content will be added.
    projects: A list of Project objects representing projects to be rendered.
    settings: The settings object that controls which parts of the projects to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, projects, and settings.
    2. Log a debug message indicating initialization.

---
## method: `RenderProjectsSection.render(self: UnknownType) -> None`

Render projects section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. If any projects exist, add a heading "Projects" at level 2.
    3. Iterate over each project in the projects list.
    4. For each project, create a RenderProjectSection instance and call its render method.

---
## `RenderExperienceSection` class

Render experience section.

---
## method: `RenderExperienceSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to which the experience content will be added.
    experience: The Experience object containing roles and projects to be rendered.
    settings: The settings object that controls which parts of experience to render.

Returns:
    None.

Notes:
    1. Initialize the base class with the provided document, experience, and settings.
    2. Log a debug message indicating initialization.

---
## method: `RenderExperienceSection.render(self: UnknownType) -> None`

Render experience section.

Args:
    None.

Returns:
    None.

Notes:
    1. Log a debug message indicating the start of rendering.
    2. If roles are enabled and the experience has roles, render them using RenderRolesSection.
    3. If projects are enabled and the experience has projects, render them using RenderProjectsSection.

---

===

===
# File: `executive_summary_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to which the executive summary will be added.
    experience: The Experience object containing role and job data to summarize.
    settings: The settings object that defines which categories to include in the summary.

Returns:
    None

Notes:
    1. Initialize the parent class (ResumeRenderExecutiveSummaryBase) with the provided document, experience, and settings.
    2. Log a debug message indicating that the functional experience render object is being initialized.

---

## function: `render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating that the functional experience section is being rendered.
    2. Check if the experience object has any roles; if not, raise a ValueError.
    3. Create an ExecutiveSummary object using the experience data.
    4. Generate the executive summary using the specified categories from the settings.
    5. For each category in the summary:
        a. Add a heading to the document with level 4.
        b. For each summary entry in the category:
            i. Create a new paragraph and apply the "List Bullet" style.
            ii. Add the summary text as a run.
            iii. If no company is available, log a warning.
            iv. If a company is available, determine the date string (either the last date formatted to year or "Present").
            v. Add an italicized run with the company and date information.
    6. This function performs no disk, network, or database access.

---

## `RenderExecutiveSummarySection` class

Render experience for a functional resume.

---
## method: `RenderExecutiveSummarySection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to which the executive summary will be added.
    experience: The Experience object containing role and job data to summarize.
    settings: The settings object that defines which categories to include in the summary.

Returns:
    None

Notes:
    1. Initialize the parent class (ResumeRenderExecutiveSummaryBase) with the provided document, experience, and settings.
    2. Log a debug message indicating that the functional experience render object is being initialized.

---
## method: `RenderExecutiveSummarySection.render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating that the functional experience section is being rendered.
    2. Check if the experience object has any roles; if not, raise a ValueError.
    3. Create an ExecutiveSummary object using the experience data.
    4. Generate the executive summary using the specified categories from the settings.
    5. For each category in the summary:
        a. Add a heading to the document with level 4.
        b. For each summary entry in the category:
            i. Create a new paragraph and apply the "List Bullet" style.
            ii. Add the summary text as a run.
            iii. If no company is available, log a warning.
            iv. If a company is available, determine the date string (either the last date formatted to year or "Present").
            v. Add an italicized run with the company and date information.
    6. This function performs no disk, network, or database access.

---

===

===
# File: `personal_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The Word document object to which content will be added.
    personal: The personal information model containing contact details, banner, note, websites, and visa status.
    settings: The rendering settings that control which sections are enabled or disabled.

Returns:
    None

Notes:
    1. Initialize the base class with the provided document, personal data, and settings.
    2. Log debug message indicating the initialization of the personal basic render object.

---

## function: `_contact_info(self: UnknownType) -> None`

Render the contact info section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of contact information.
    2. Extract the contact info from the personal data.
    3. If the name is present and enabled in settings, add "Name: <name>" to the list.
    4. If the email is present and enabled in settings, add "Email: <email>" to the list.
    5. If the phone is present and enabled in settings, add "Phone: <phone>" to the list.
    6. If the location is present and enabled in settings, add "Location: <location>" to the list.
    7. If any lines were added, join them with newlines and add the combined text as a paragraph in the document.

---

## function: `_banner(self: UnknownType) -> None`

Render the banner section.

Args:
    None

Returns:
    None

Notes:
    1. Extract the banner text from the personal data.
    2. If the banner text is present, add a level 3 heading titled "Banner".
    3. Add the banner text as a paragraph immediately after the heading.

---

## function: `_note(self: UnknownType) -> None`

Render the note section.

Args:
    None

Returns:
    None

Notes:
    1. Extract the note text from the personal data.
    2. If the note text is present, add a level 3 heading titled "Note".
    3. Add the note text as a paragraph immediately after the heading.

---

## function: `_websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of website information.
    2. Extract the websites data from the personal data.
    3. If GitHub URL is present and enabled in settings, add "GitHub: <url>" to the list.
    4. If LinkedIn URL is present and enabled in settings, add "LinkedIn: <url>" to the list.
    5. If personal website URL is present and enabled in settings, add "Website: <url>" to the list.
    6. If Twitter URL is present and enabled in settings, add "Twitter: <url>" to the list.
    7. If any lines were added, add a level 3 heading titled "Websites".
    8. Join the lines with newlines and add the combined text as a paragraph in the document.

---

## function: `_visa_status(self: UnknownType) -> None`

Render the visa status section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of visa status information.
    2. Extract the visa status data from the personal data.
    3. If work authorization is present and enabled in settings, add "Work Authorization: <status>" to the list.
    4. If sponsorship requirement is defined and enabled in settings, determine the value ("Yes" if True, "No" if False) and add "Require Sponsorship: <value>" to the list.
    5. If any lines were added, add a level 3 heading titled "Visa Status".
    6. Join the lines with newlines and add the combined text as a paragraph in the document.

---

## function: `render(self: UnknownType) -> None`

Render the personal section.

Args:
    None

Returns:
    None

Notes:
    1. If contact info exists and is enabled in settings, render the contact info section.
    2. If banner exists and is enabled in settings, render the banner section.
    3. If note exists and is enabled in settings, render the note section.
    4. If websites exist and are enabled in settings, render the websites section.
    5. If visa status exists and is enabled in settings, render the visa status section.

---

## `RenderPersonalSection` class

Render personal contact info section.

---
## method: `RenderPersonalSection.__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The Word document object to which content will be added.
    personal: The personal information model containing contact details, banner, note, websites, and visa status.
    settings: The rendering settings that control which sections are enabled or disabled.

Returns:
    None

Notes:
    1. Initialize the base class with the provided document, personal data, and settings.
    2. Log debug message indicating the initialization of the personal basic render object.

---
## method: `RenderPersonalSection._contact_info(self: UnknownType) -> None`

Render the contact info section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of contact information.
    2. Extract the contact info from the personal data.
    3. If the name is present and enabled in settings, add "Name: <name>" to the list.
    4. If the email is present and enabled in settings, add "Email: <email>" to the list.
    5. If the phone is present and enabled in settings, add "Phone: <phone>" to the list.
    6. If the location is present and enabled in settings, add "Location: <location>" to the list.
    7. If any lines were added, join them with newlines and add the combined text as a paragraph in the document.

---
## method: `RenderPersonalSection._banner(self: UnknownType) -> None`

Render the banner section.

Args:
    None

Returns:
    None

Notes:
    1. Extract the banner text from the personal data.
    2. If the banner text is present, add a level 3 heading titled "Banner".
    3. Add the banner text as a paragraph immediately after the heading.

---
## method: `RenderPersonalSection._note(self: UnknownType) -> None`

Render the note section.

Args:
    None

Returns:
    None

Notes:
    1. Extract the note text from the personal data.
    2. If the note text is present, add a level 3 heading titled "Note".
    3. Add the note text as a paragraph immediately after the heading.

---
## method: `RenderPersonalSection._websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of website information.
    2. Extract the websites data from the personal data.
    3. If GitHub URL is present and enabled in settings, add "GitHub: <url>" to the list.
    4. If LinkedIn URL is present and enabled in settings, add "LinkedIn: <url>" to the list.
    5. If personal website URL is present and enabled in settings, add "Website: <url>" to the list.
    6. If Twitter URL is present and enabled in settings, add "Twitter: <url>" to the list.
    7. If any lines were added, add a level 3 heading titled "Websites".
    8. Join the lines with newlines and add the combined text as a paragraph in the document.

---
## method: `RenderPersonalSection._visa_status(self: UnknownType) -> None`

Render the visa status section.

Args:
    None

Returns:
    None

Notes:
    1. Initialize an empty list to hold lines of visa status information.
    2. Extract the visa status data from the personal data.
    3. If work authorization is present and enabled in settings, add "Work Authorization: <status>" to the list.
    4. If sponsorship requirement is defined and enabled in settings, determine the value ("Yes" if True, "No" if False) and add "Require Sponsorship: <value>" to the list.
    5. If any lines were added, add a level 3 heading titled "Visa Status".
    6. Join the lines with newlines and add the combined text as a paragraph in the document.

---
## method: `RenderPersonalSection.render(self: UnknownType) -> None`

Render the personal section.

Args:
    None

Returns:
    None

Notes:
    1. If contact info exists and is enabled in settings, render the contact info section.
    2. If banner exists and is enabled in settings, render the banner section.
    3. If note exists and is enabled in settings, render the note section.
    4. If websites exist and are enabled in settings, render the websites section.
    5. If visa status exists and is enabled in settings, render the visa status section.

---

===

===
# File: `resume_main.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The Word document object to render the resume into.
    resume: The resume data model containing personal, education, experience, certifications, and other sections.
    settings: Configuration settings for rendering specific sections of the resume.

Notes:
    1. The super().__init__() method is called to initialize the base class with the provided document, resume, and settings.
    2. No external file, network, or database access occurs during initialization.

---

## function: `render(self: UnknownType) -> None`

Render the resume by conditionally adding sections based on data and settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. Check if the resume has personal information and if the personal section is enabled in settings.
    2. If both conditions are true, render the personal section using RenderPersonalSection.
    3. Check if the resume has education data and if the education section is enabled in settings.
    4. If both conditions are true, render the education section using RenderEducationSection.
    5. Check if the resume has certifications and if the certifications section is enabled in settings.
    6. If both conditions are true, render the certifications section using RenderCertificationsSection.
    7. Check if the resume has experience data and if the executive summary section is enabled in settings.
    8. If both conditions are true, add a heading titled "Executive Summary" and render the summary using RenderExecutiveSummarySection.
    9. Check if the resume has experience data and if the skills matrix section is enabled in settings.
    10. If both conditions are true, render the skills matrix section using RenderSkillsMatrixSection.
    11. Check if the resume has experience data and if the experience section is enabled in settings.
    12. If both conditions are true, render the experience section using RenderExperienceSection.
    13. No external file, network, or database access occurs during rendering.

---

## `RenderResume` class

Render a resume in basic format.

---
## method: `RenderResume.__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The Word document object to render the resume into.
    resume: The resume data model containing personal, education, experience, certifications, and other sections.
    settings: Configuration settings for rendering specific sections of the resume.

Notes:
    1. The super().__init__() method is called to initialize the base class with the provided document, resume, and settings.
    2. No external file, network, or database access occurs during initialization.

---
## method: `RenderResume.render(self: UnknownType) -> None`

Render the resume by conditionally adding sections based on data and settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. Check if the resume has personal information and if the personal section is enabled in settings.
    2. If both conditions are true, render the personal section using RenderPersonalSection.
    3. Check if the resume has education data and if the education section is enabled in settings.
    4. If both conditions are true, render the education section using RenderEducationSection.
    5. Check if the resume has certifications and if the certifications section is enabled in settings.
    6. If both conditions are true, render the certifications section using RenderCertificationsSection.
    7. Check if the resume has experience data and if the executive summary section is enabled in settings.
    8. If both conditions are true, add a heading titled "Executive Summary" and render the summary using RenderExecutiveSummarySection.
    9. Check if the resume has experience data and if the skills matrix section is enabled in settings.
    10. If both conditions are true, render the skills matrix section using RenderSkillsMatrixSection.
    11. Check if the resume has experience data and if the experience section is enabled in settings.
    12. If both conditions are true, render the experience section using RenderExperienceSection.
    13. No external file, network, or database access occurs during rendering.

---

===

===
# File: `skills_matrix_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> UnknownType`

Initialize skills render object.

Args:
    document: The DOCX document to which the skills section will be added.
    experience: The experience data containing roles and skill usage history.
    settings: Configuration settings for rendering the skills matrix.
    parse_context: Contextual information used during parsing, not directly used here.

Returns:
    None

Notes:
    1. Validate that the provided parse_context is an instance of ParseContext.
    2. Store the parse_context for potential future use.
    3. Initialize the parent class (ResumeRenderSkillsMatrixBase) with the given parameters.

---

## function: `render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object has any roles; if not, raise a ValueError.
    2. Create a SkillsMatrix instance from the experience roles.
    3. If settings.all_skills is True, generate a matrix for all skills using the special value "*all*".
    4. Otherwise, generate a matrix only for the skills specified in settings.skills.
    5. Calculate the number of rows needed for the table based on the number of skills (each row holds two skills).
    6. Create a new table with the calculated number of rows and 4 columns, using the "Table Grid" style.
    7. Add a header row with bolded column titles: "Skill", "YOE (from - to)", "Skill", "YOE (from - to)".
    8. Iterate through the sorted skills and their data.
    9. For each skill, determine its row and column position in the table.
    10. Insert the skill name into the appropriate cell and center it vertically.
    11. Format the YOE string using the first_used and last_used dates, along with the calculated YOE value.
    12. Insert the formatted YOE string into the adjacent cell.
    13. Set the table to auto-fit its contents.

---

## `RenderSkillsMatrixSection` class

Render skills for a functional resume.

---
## method: `RenderSkillsMatrixSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> UnknownType`

Initialize skills render object.

Args:
    document: The DOCX document to which the skills section will be added.
    experience: The experience data containing roles and skill usage history.
    settings: Configuration settings for rendering the skills matrix.
    parse_context: Contextual information used during parsing, not directly used here.

Returns:
    None

Notes:
    1. Validate that the provided parse_context is an instance of ParseContext.
    2. Store the parse_context for potential future use.
    3. Initialize the parent class (ResumeRenderSkillsMatrixBase) with the given parameters.

---
## method: `RenderSkillsMatrixSection.render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object has any roles; if not, raise a ValueError.
    2. Create a SkillsMatrix instance from the experience roles.
    3. If settings.all_skills is True, generate a matrix for all skills using the special value "*all*".
    4. Otherwise, generate a matrix only for the skills specified in settings.skills.
    5. Calculate the number of rows needed for the table based on the number of skills (each row holds two skills).
    6. Create a new table with the calculated number of rows and 4 columns, using the "Table Grid" style.
    7. Add a header row with bolded column titles: "Skill", "YOE (from - to)", "Skill", "YOE (from - to)".
    8. Iterate through the sorted skills and their data.
    9. For each skill, determine its row and column position in the table.
    10. Insert the skill name into the appropriate cell and center it vertically.
    11. Format the YOE string using the first_used and last_used dates, along with the calculated YOE value.
    12. Insert the formatted YOE string into the adjacent cell.
    13. Set the table to auto-fit its contents.

---

===

===
# File: `education_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

Args:
    document: The Word document to render the degree section into.
    degree: The degree object containing education details such as school, degree name, dates, major, and GPA.
    settings: Configuration settings that control which degree fields are rendered (e.g., school, degree, dates, major, GPA).

Returns:
    None

Notes:
    1. Store the provided document, degree, and settings as instance attributes.
    2. No disk, network, or database access occurs during initialization.

---

## function: `render(self: UnknownType) -> None`

Render a single degree.

Args:
    None

Returns:
    None

Notes:
    1. Create a new paragraph in the document to hold the degree details.
    2. If the school name is present and enabled in settings, add it in bold, underlined, and larger font size.
    3. If the degree name is present and enabled in settings, add it in bold.
    4. If the start date is present and enabled in settings, format it as "Month Year" and add it.
    5. If the end date is present and enabled in settings, format it as "Month Year" (or "Present" if None) and add it.
    6. If the major is present and enabled in settings, add it.
    7. If the GPA is present and enabled in settings, add it in the format "GPA: X.XX".
    8. All text additions use runs and breaks to format the output properly.
    9. No disk, network, or database access occurs during rendering.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

Args:
    document: The Word document to render the education section into.
    education: The education object containing a list of degrees and related data.
    settings: Configuration settings that control rendering behavior, including whether to render degrees and which fields to include.

Returns:
    None

Notes:
    1. Store the provided document, education, and settings as instance attributes.
    2. No disk, network, or database access occurs during initialization.

---

## function: `render(self: UnknownType) -> None`

Render the education section.

Args:
    None

Returns:
    None

Notes:
    1. If the 'degrees' setting is disabled, exit early without rendering.
    2. Add a level-2 heading titled "Education" to the document.
    3. For each degree in the education object, create a RenderDegreeSection instance and call its render method.
    4. Rendering each degree is delegated to the RenderDegreeSection class.
    5. No disk, network, or database access occurs during rendering.

---

## `RenderDegreeSection` class

Render Degree Section.

---
## method: `RenderDegreeSection.__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

Args:
    document: The Word document to render the degree section into.
    degree: The degree object containing education details such as school, degree name, dates, major, and GPA.
    settings: Configuration settings that control which degree fields are rendered (e.g., school, degree, dates, major, GPA).

Returns:
    None

Notes:
    1. Store the provided document, degree, and settings as instance attributes.
    2. No disk, network, or database access occurs during initialization.

---
## method: `RenderDegreeSection.render(self: UnknownType) -> None`

Render a single degree.

Args:
    None

Returns:
    None

Notes:
    1. Create a new paragraph in the document to hold the degree details.
    2. If the school name is present and enabled in settings, add it in bold, underlined, and larger font size.
    3. If the degree name is present and enabled in settings, add it in bold.
    4. If the start date is present and enabled in settings, format it as "Month Year" and add it.
    5. If the end date is present and enabled in settings, format it as "Month Year" (or "Present" if None) and add it.
    6. If the major is present and enabled in settings, add it.
    7. If the GPA is present and enabled in settings, add it in the format "GPA: X.XX".
    8. All text additions use runs and breaks to format the output properly.
    9. No disk, network, or database access occurs during rendering.

---
## `RenderEducationSection` class

Render Education Section.

---
## method: `RenderEducationSection.__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

Args:
    document: The Word document to render the education section into.
    education: The education object containing a list of degrees and related data.
    settings: Configuration settings that control rendering behavior, including whether to render degrees and which fields to include.

Returns:
    None

Notes:
    1. Store the provided document, education, and settings as instance attributes.
    2. No disk, network, or database access occurs during initialization.

---
## method: `RenderEducationSection.render(self: UnknownType) -> None`

Render the education section.

Args:
    None

Returns:
    None

Notes:
    1. If the 'degrees' setting is disabled, exit early without rendering.
    2. Add a level-2 heading titled "Education" to the document.
    3. For each degree in the education object, create a RenderDegreeSection instance and call its render method.
    4. Rendering each degree is delegated to the RenderDegreeSection class.
    5. No disk, network, or database access occurs during rendering.

---

===

===
# File: `resume_main.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize ATS resume renderer.

Args:
    document: The Word document object to render the resume into.
    resume: The parsed resume data structure containing personal, education,
            experience, certifications, and other sections.
    settings: Configuration settings for rendering the resume, including
              which sections to include and how they should be formatted.

Notes:
    1. Calls the parent class constructor to initialize common rendering state.
    2. Applies default settings overrides specific to ATS resume formatting.

---

## function: `_settings_override(self: UnknownType) -> None`

Apply default settings overrides for ATS resumes.

Args:
    None

Returns:
    None

Notes:
    1. Disables the inclusion of role summaries in the experience section.
    2. Disables the executive summary section.
    3. Disables the skills matrix section.
    4. These settings are enforced to ensure compatibility with applicant tracking systems.

---

## function: `render(self: UnknownType) -> None`

Render the resume by processing each enabled section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if personal information exists and the personal section is enabled.
    2. If enabled, renders the personal section using RenderPersonalSection.
    3. Checks if education data exists and the education section is enabled.
    4. If enabled, renders the education section using RenderEducationSection.
    5. Checks if certifications exist and the certifications section is enabled.
    6. If enabled, renders the certifications section using RenderCertificationsSection.
    7. Checks if experience data exists and the executive summary is enabled.
    8. If enabled, adds a heading "Executive Summary" and renders the summary using RenderExecutiveSummarySection.
    9. Checks if experience data exists and the skills matrix is enabled.
    10. If enabled, renders the skills matrix using RenderSkillsMatrixSection.
    11. Checks if experience data exists and the experience section is enabled.
    12. If enabled, renders the experience section using RenderExperienceSection.

---

## `RenderResume` class

Render a resume in basic format.

---
## method: `RenderResume.__init__(self: UnknownType, document: docx.document.Document, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize ATS resume renderer.

Args:
    document: The Word document object to render the resume into.
    resume: The parsed resume data structure containing personal, education,
            experience, certifications, and other sections.
    settings: Configuration settings for rendering the resume, including
              which sections to include and how they should be formatted.

Notes:
    1. Calls the parent class constructor to initialize common rendering state.
    2. Applies default settings overrides specific to ATS resume formatting.

---
## method: `RenderResume._settings_override(self: UnknownType) -> None`

Apply default settings overrides for ATS resumes.

Args:
    None

Returns:
    None

Notes:
    1. Disables the inclusion of role summaries in the experience section.
    2. Disables the executive summary section.
    3. Disables the skills matrix section.
    4. These settings are enforced to ensure compatibility with applicant tracking systems.

---
## method: `RenderResume.render(self: UnknownType) -> None`

Render the resume by processing each enabled section.

Args:
    None

Returns:
    None

Notes:
    1. Checks if personal information exists and the personal section is enabled.
    2. If enabled, renders the personal section using RenderPersonalSection.
    3. Checks if education data exists and the education section is enabled.
    4. If enabled, renders the education section using RenderEducationSection.
    5. Checks if certifications exist and the certifications section is enabled.
    6. If enabled, renders the certifications section using RenderCertificationsSection.
    7. Checks if experience data exists and the executive summary is enabled.
    8. If enabled, adds a heading "Executive Summary" and renders the summary using RenderExecutiveSummarySection.
    9. Checks if experience data exists and the skills matrix is enabled.
    10. If enabled, renders the skills matrix using RenderSkillsMatrixSection.
    11. Checks if experience data exists and the experience section is enabled.
    12. If enabled, renders the experience section using RenderExperienceSection.

---

===

===
# File: `experience_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to render into.
    role: The role data to render.
    settings: The settings for rendering the role.

---

## function: `_skills(self: UnknownType) -> list[str]`

Render role skills section.

Returns:
    A list of strings containing the formatted skills text.

Notes:
    1. Initialize an empty list to store the output lines.
    2. Check if the role has skills and the settings allow rendering skills.
    3. If skills exist, join them into a comma-separated string.
    4. Append the formatted "Skills: <skills>" string to the output list.
    5. Return the list of formatted skill lines.

---

## function: `_details(self: UnknownType) -> list[str]`

Render role details section.

Returns:
    A list of strings containing the formatted detail lines.

Notes:
    1. Initialize an empty list to store the output lines.
    2. Extract the basics information from the role.
    3. If job category is present and enabled in settings, append it to the output list.
    4. If location is present and enabled in settings, append it to the output list.
    5. If agency name is present and enabled in settings, append it to the output list.
    6. If employment type is present and enabled in settings, append it to the output list.
    7. Return the list of formatted detail lines.

---

## function: `_dates(self: UnknownType) -> str`

Generate dates string for role.

Returns:
    A formatted string containing start date and optional end date.

Notes:
    1. Extract the basics information from the role.
    2. If start date is missing, log a warning and append an error.
    3. Format the start date as "mm-YYYY".
    4. If end date is present, format it as "mm-YYYY" and append to the string.
    5. If end date is missing, append " - Present" to the string.
    6. Return the final formatted date string.

---

## function: `render(self: UnknownType) -> None`

Render role overview/basics section.

Notes:
    1. Initialize an empty list to store paragraph lines.
    2. Create a paragraph for the role basics.
    3. If company name is missing, log an error and append to errors list.
    4. Add the company name as bold and underlined text with increased font size.
    5. Insert a line break.
    6. If title is missing, log an error and append to errors list.
    7. Add the title as bold text.
    8. Insert a line break.
    9. Generate and add the formatted dates to the paragraph.
    10. Create a paragraph for the details section.
    11. Collect and clean the detail lines.
    12. If any detail lines exist, add them to the details paragraph.
    13. If summary is present and enabled, add it as italicized text with spacing.
    14. If responsibilities are present and enabled, add them with spacing.
    15. If skills are present and enabled, add them with spacing.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to render into.
    roles: The list of role data to render.
    settings: The settings for rendering the roles.

---

## function: `render(self: UnknownType) -> None`

Render roles section.

Notes:
    1. If no roles are present, log info and return.
    2. Add a heading "Work History" with level 2.
    3. For each role:
    4. If it's the first role, add a horizontal line.
    5. Render the role using RenderRoleSection.
    6. If it's not the last role, add a horizontal line and a blank paragraph.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The Docx document object to render into.
    project: The project data to render.
    settings: The settings for rendering the project.

---

## function: `_overview(self: UnknownType) -> list[str]`

Render project overview section.

Returns:
    A list of strings containing the formatted overview lines.

Notes:
    1. Initialize an empty list to store output lines.
    2. Extract the project overview data.
    3. If URL description and URL are present and enabled, create a formatted URL line.
    4. If start date is present and enabled, format it and append.
    5. If end date is present and enabled, format it and append.
    6. Return the list of formatted lines.

---

## function: `_skills(self: UnknownType) -> list[str]`

Render project skills section.

Returns:
    A list of strings containing the formatted skills text.

Notes:
    1. Initialize an empty list to store output lines.
    2. Join the project skills into a comma-separated string.
    3. Append the formatted "Skills: <skills>" string to the output list.
    4. Return the list of formatted skill lines.

---

## function: `render(self: UnknownType) -> None`

Render project section.

Notes:
    1. Initialize an empty list to store paragraph lines.
    2. If overview is present and enabled, collect its lines.
    3. If description is present and enabled, add it to the lines.
    4. If skills are present and enabled, collect their lines.
    5. If any lines exist, add them to the document as a single paragraph.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The Docx document object to render into.
    projects: The list of project data to render.
    settings: The settings for rendering the projects.

---

## function: `render(self: UnknownType) -> None`

Render projects section.

Notes:
    1. If no projects are present, log info and return.
    2. Add a heading "Projects" with level 2.
    3. For each project:
    4. Create a RenderProjectSection object.
    5. Render the project.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to render into.
    experience: The experience data to render.
    settings: The settings for rendering the experience.

---

## function: `render(self: UnknownType) -> None`

Render experience section.

Notes:
    1. If roles are present and enabled, render the roles section.
    2. If projects are present and enabled, render the projects section.

---

## `RenderRoleSection` class

Render experience roles section.

---
## method: `RenderRoleSection.__init__(self: UnknownType, document: docx.document.Document, role: Role, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to render into.
    role: The role data to render.
    settings: The settings for rendering the role.

---
## method: `RenderRoleSection._skills(self: UnknownType) -> list[str]`

Render role skills section.

Returns:
    A list of strings containing the formatted skills text.

Notes:
    1. Initialize an empty list to store the output lines.
    2. Check if the role has skills and the settings allow rendering skills.
    3. If skills exist, join them into a comma-separated string.
    4. Append the formatted "Skills: <skills>" string to the output list.
    5. Return the list of formatted skill lines.

---
## method: `RenderRoleSection._details(self: UnknownType) -> list[str]`

Render role details section.

Returns:
    A list of strings containing the formatted detail lines.

Notes:
    1. Initialize an empty list to store the output lines.
    2. Extract the basics information from the role.
    3. If job category is present and enabled in settings, append it to the output list.
    4. If location is present and enabled in settings, append it to the output list.
    5. If agency name is present and enabled in settings, append it to the output list.
    6. If employment type is present and enabled in settings, append it to the output list.
    7. Return the list of formatted detail lines.

---
## method: `RenderRoleSection._dates(self: UnknownType) -> str`

Generate dates string for role.

Returns:
    A formatted string containing start date and optional end date.

Notes:
    1. Extract the basics information from the role.
    2. If start date is missing, log a warning and append an error.
    3. Format the start date as "mm-YYYY".
    4. If end date is present, format it as "mm-YYYY" and append to the string.
    5. If end date is missing, append " - Present" to the string.
    6. Return the final formatted date string.

---
## method: `RenderRoleSection.render(self: UnknownType) -> None`

Render role overview/basics section.

Notes:
    1. Initialize an empty list to store paragraph lines.
    2. Create a paragraph for the role basics.
    3. If company name is missing, log an error and append to errors list.
    4. Add the company name as bold and underlined text with increased font size.
    5. Insert a line break.
    6. If title is missing, log an error and append to errors list.
    7. Add the title as bold text.
    8. Insert a line break.
    9. Generate and add the formatted dates to the paragraph.
    10. Create a paragraph for the details section.
    11. Collect and clean the detail lines.
    12. If any detail lines exist, add them to the details paragraph.
    13. If summary is present and enabled, add it as italicized text with spacing.
    14. If responsibilities are present and enabled, add them with spacing.
    15. If skills are present and enabled, add them with spacing.

---
## `RenderRolesSection` class

Render experience roles section.

---
## method: `RenderRolesSection.__init__(self: UnknownType, document: docx.document.Document, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The Docx document object to render into.
    roles: The list of role data to render.
    settings: The settings for rendering the roles.

---
## method: `RenderRolesSection.render(self: UnknownType) -> None`

Render roles section.

Notes:
    1. If no roles are present, log info and return.
    2. Add a heading "Work History" with level 2.
    3. For each role:
    4. If it's the first role, add a horizontal line.
    5. Render the role using RenderRoleSection.
    6. If it's not the last role, add a horizontal line and a blank paragraph.

---
## `RenderProjectSection` class

Render experience project section.

---
## method: `RenderProjectSection.__init__(self: UnknownType, document: docx.document.Document, project: Project, settings: ResumeProjectsSettings) -> UnknownType`

Initialize project render object.

Args:
    document: The Docx document object to render into.
    project: The project data to render.
    settings: The settings for rendering the project.

---
## method: `RenderProjectSection._overview(self: UnknownType) -> list[str]`

Render project overview section.

Returns:
    A list of strings containing the formatted overview lines.

Notes:
    1. Initialize an empty list to store output lines.
    2. Extract the project overview data.
    3. If URL description and URL are present and enabled, create a formatted URL line.
    4. If start date is present and enabled, format it and append.
    5. If end date is present and enabled, format it and append.
    6. Return the list of formatted lines.

---
## method: `RenderProjectSection._skills(self: UnknownType) -> list[str]`

Render project skills section.

Returns:
    A list of strings containing the formatted skills text.

Notes:
    1. Initialize an empty list to store output lines.
    2. Join the project skills into a comma-separated string.
    3. Append the formatted "Skills: <skills>" string to the output list.
    4. Return the list of formatted skill lines.

---
## method: `RenderProjectSection.render(self: UnknownType) -> None`

Render project section.

Notes:
    1. Initialize an empty list to store paragraph lines.
    2. If overview is present and enabled, collect its lines.
    3. If description is present and enabled, add it to the lines.
    4. If skills are present and enabled, collect their lines.
    5. If any lines exist, add them to the document as a single paragraph.

---
## `RenderProjectsSection` class

Render experience projects section.

---
## method: `RenderProjectsSection.__init__(self: UnknownType, document: docx.document.Document, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The Docx document object to render into.
    projects: The list of project data to render.
    settings: The settings for rendering the projects.

---
## method: `RenderProjectsSection.render(self: UnknownType) -> None`

Render projects section.

Notes:
    1. If no projects are present, log info and return.
    2. Add a heading "Projects" with level 2.
    3. For each project:
    4. Create a RenderProjectSection object.
    5. Render the project.

---
## `RenderExperienceSection` class

Render experience section.

---
## method: `RenderExperienceSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The Docx document object to render into.
    experience: The experience data to render.
    settings: The settings for rendering the experience.

---
## method: `RenderExperienceSection.render(self: UnknownType) -> None`

Render experience section.

Notes:
    1. If roles are present and enabled, render the roles section.
    2. If projects are present and enabled, render the projects section.

---

===

===
# File: `executive_summary_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document: The Word document object to which the executive summary will be added.
    experience: The experience data containing roles and related information.
    settings: Configuration settings for rendering the executive summary section.

Returns:
    None

Notes:
    1. Initialize the parent class with the provided document, experience, and settings.
    2. Log a debug message indicating the initialization of the functional experience render object.

---

## function: `render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating the start of rendering the functional experience section.
    2. Validate that the experience object contains at least one role; raise a ValueError if not.
    3. Collect all unique job categories from the roles in the experience.
    4. For each job category specified in the settings:
        a. Filter roles belonging to the current category.
        b. If no roles are found for the category, log a warning and skip to the next category.
        c. Add a heading for the category with level 4.
        d. For each role in the category:
            i. If no summary is available for the role, log a warning and skip to the next role.
            ii. If no company is available for the role, log a warning and skip to the next role.
            iii. Create a new paragraph with the bullet style.
            iv. Add the role summary as a run to the paragraph.
            v. Add the company name in italic as a run to the paragraph, appended to the summary.

---

## `RenderExecutiveSummarySection` class

Render experience for a functional resume.

---
## method: `RenderExecutiveSummarySection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize experience render object.

Args:
    document: The Word document object to which the executive summary will be added.
    experience: The experience data containing roles and related information.
    settings: Configuration settings for rendering the executive summary section.

Returns:
    None

Notes:
    1. Initialize the parent class with the provided document, experience, and settings.
    2. Log a debug message indicating the initialization of the functional experience render object.

---
## method: `RenderExecutiveSummarySection.render(self: UnknownType) -> None`

Render experience section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating the start of rendering the functional experience section.
    2. Validate that the experience object contains at least one role; raise a ValueError if not.
    3. Collect all unique job categories from the roles in the experience.
    4. For each job category specified in the settings:
        a. Filter roles belonging to the current category.
        b. If no roles are found for the category, log a warning and skip to the next category.
        c. Add a heading for the category with level 4.
        d. For each role in the category:
            i. If no summary is available for the role, log a warning and skip to the next role.
            ii. If no company is available for the role, log a warning and skip to the next role.
            iii. Create a new paragraph with the bullet style.
            iv. Add the role summary as a run to the paragraph.
            v. Add the company name in italic as a run to the paragraph, appended to the summary.

---

===

===
# File: `education_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

---

## function: `render(self: UnknownType) -> None`

Render a single degree.

This method constructs and adds a formatted paragraph to the document
representing a single degree, including school, degree, dates, major, and GPA
as specified by the settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return a value.

Notes:
    1. Logs debugging information about the rendering process.
    2. Creates a new paragraph in the document.
    3. Adds the school name (if enabled and present) with bold, underline, and increased font size.
    4. Adds a line break after the school name.
    5. Adds the degree name (if enabled and present) in bold.
    6. Adds a line break after the degree name.
    7. Adds the start date (if enabled and present) in "Month Year" format.
    8. Adds a " - " separator if the end date will be rendered.
    9. Adds a line break after the start date if no end date is rendered.
    10. Adds the end date (if enabled and present) in "Month Year" format or "Present" if no end date is provided.
    11. Adds a line break after the end date.
    12. Adds the major (if enabled and present).
    13. Adds a line break after the major.
    14. Adds the GPA (if enabled and present) with the label "GPA: ".
    15. The method does not perform any disk, network, or database access.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

---

## function: `render(self: UnknownType) -> None`

Render the education section.

This method adds a formatted heading and a list of degree sections to the document,
using the provided education data and rendering settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return a value.

Notes:
    1. Logs debugging information about the rendering process.
    2. Checks if the degrees setting is disabled; if so, returns early.
    3. Adds a heading "Education" at level 2 to the document.
    4. Iterates through each degree in the education's degrees list.
    5. For each degree, instantiates a RenderDegreeSection and calls its render method.
    6. Adds a blank paragraph after each degree except the last one to provide visual separation.
    7. The method does not perform any disk, network, or database access.

---

## `RenderDegreeSection` class

Render a single academic degree section in a resume document.

This class is responsible for formatting and adding a single degree's details
to a Word document, including school name, degree type, dates, major, and GPA
based on the provided settings.

Args:
    document (docx.document.Document): The Word document object to which the degree section will be added.
    degree (Degree): The Degree object containing the academic details (school, degree, dates, major, GPA).
    settings (ResumeEducationSettings): Configuration object specifying which fields to render.

Returns:
    None: This method does not return a value.

Notes:
    1. The method initializes the rendering process for a single degree.
    2. It adds a paragraph to the document.
    3. If the school name is present and the school setting is enabled, it adds the school name in bold, underlined, and slightly larger font.
    4. If the degree name is present and the degree setting is enabled, it adds the degree name in bold.
    5. If the start date is present and the start date setting is enabled, it formats and adds the start date (e.g., "January 2020").
    6. If the end date is present and the end date setting is enabled, it formats and adds the end date (e.g., "December 2024") or "Present" if no end date is provided.
    7. If the major is present and the major setting is enabled, it adds the major name.
    8. If the GPA is present and the GPA setting is enabled, it adds the GPA label and value.
    9. The method does not perform any disk, network, or database access.

---
## method: `RenderDegreeSection.__init__(self: UnknownType, document: docx.document.Document, degree: Degree, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic degree renderer.

---
## method: `RenderDegreeSection.render(self: UnknownType) -> None`

Render a single degree.

This method constructs and adds a formatted paragraph to the document
representing a single degree, including school, degree, dates, major, and GPA
as specified by the settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return a value.

Notes:
    1. Logs debugging information about the rendering process.
    2. Creates a new paragraph in the document.
    3. Adds the school name (if enabled and present) with bold, underline, and increased font size.
    4. Adds a line break after the school name.
    5. Adds the degree name (if enabled and present) in bold.
    6. Adds a line break after the degree name.
    7. Adds the start date (if enabled and present) in "Month Year" format.
    8. Adds a " - " separator if the end date will be rendered.
    9. Adds a line break after the start date if no end date is rendered.
    10. Adds the end date (if enabled and present) in "Month Year" format or "Present" if no end date is provided.
    11. Adds a line break after the end date.
    12. Adds the major (if enabled and present).
    13. Adds a line break after the major.
    14. Adds the GPA (if enabled and present) with the label "GPA: ".
    15. The method does not perform any disk, network, or database access.

---
## `RenderEducationSection` class

Render the Education section of a resume in a Word document.

This class is responsible for formatting and adding an entire education section
to a Word document, including a heading and a list of rendered degree sections
based on the provided settings.

Args:
    document (docx.document.Document): The Word document object to which the education section will be added.
    education (Education): The Education object containing a list of Degree objects.
    settings (ResumeEducationSettings): Configuration object specifying which fields to render.

Returns:
    None: This method does not return a value.

Notes:
    1. Logs debugging information about the rendering process.
    2. Checks if the degrees setting is disabled; if so, returns early without rendering.
    3. Adds a level-2 heading labeled "Education" to the document.
    4. Iterates over each degree in the education's degrees list.
    5. For each degree, creates and calls RenderDegreeSection to render that degree.
    6. Adds a blank paragraph between degrees to separate them visually, except after the last degree.
    7. The method does not perform any disk, network, or database access.

---
## method: `RenderEducationSection.__init__(self: UnknownType, document: docx.document.Document, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

---
## method: `RenderEducationSection.render(self: UnknownType) -> None`

Render the education section.

This method adds a formatted heading and a list of degree sections to the document,
using the provided education data and rendering settings.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return a value.

Notes:
    1. Logs debugging information about the rendering process.
    2. Checks if the degrees setting is disabled; if so, returns early.
    3. Adds a heading "Education" at level 2 to the document.
    4. Iterates through each degree in the education's degrees list.
    5. For each degree, instantiates a RenderDegreeSection and calls its render method.
    6. Adds a blank paragraph after each degree except the last one to provide visual separation.
    7. The method does not perform any disk, network, or database access.

---

===

===
# File: `certifications_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document (docx.document.Document): The Word document to which the certification will be added.
    certification (Certification): The certification object containing details such as name, issuer, issued date, and expiration date.
    settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize common attributes.

---

## function: `render(self: UnknownType) -> None`

Render the certification section in the document.

Args:
    None: This method does not accept any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. Initializes an empty list to store lines of text for the certification.
    2. If the certification name exists and the name setting is enabled, adds the name to the lines.
    3. If the issuer exists and the issuer setting is enabled, adds the issuer to the lines.
    4. If the issued date exists and the issued setting is enabled, formats the date to "Month Year" and adds it to the lines.
    5. If the expiration date exists and the expires setting is enabled, formats the date to "Month Year" and adds it to the lines.
    6. If any lines were generated, joins them with newline characters and adds the resulting paragraph to the document.

---

## function: `__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document (docx.document.Document): The Word document to which the certifications section will be added.
    certifications (Certifications): A collection of Certification objects to be rendered.
    settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display for each certification.

Notes:
    1. Calls the parent class constructor to initialize common attributes.

---

## function: `render(self: UnknownType) -> None`

Render the certifications section in the document.

Args:
    None: This method does not accept any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. If there are certifications to render, adds a level-2 heading titled "Certifications".
    2. Iterates through each certification in the collection.
    3. For each certification, creates a RenderCertificationSection instance and renders it into the document.

---

## `RenderCertificationSection` class

Render Certification Section.

---
## method: `RenderCertificationSection.__init__(self: UnknownType, document: docx.document.Document, certification: Certification, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certification renderer.

Args:
    document (docx.document.Document): The Word document to which the certification will be added.
    certification (Certification): The certification object containing details such as name, issuer, issued date, and expiration date.
    settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display in the rendered output.

Notes:
    1. Calls the parent class constructor to initialize common attributes.

---
## method: `RenderCertificationSection.render(self: UnknownType) -> None`

Render the certification section in the document.

Args:
    None: This method does not accept any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. Initializes an empty list to store lines of text for the certification.
    2. If the certification name exists and the name setting is enabled, adds the name to the lines.
    3. If the issuer exists and the issuer setting is enabled, adds the issuer to the lines.
    4. If the issued date exists and the issued setting is enabled, formats the date to "Month Year" and adds it to the lines.
    5. If the expiration date exists and the expires setting is enabled, formats the date to "Month Year" and adds it to the lines.
    6. If any lines were generated, joins them with newline characters and adds the resulting paragraph to the document.

---
## `RenderCertificationsSection` class

Render Certifications Section.

---
## method: `RenderCertificationsSection.__init__(self: UnknownType, document: docx.document.Document, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document (docx.document.Document): The Word document to which the certifications section will be added.
    certifications (Certifications): A collection of Certification objects to be rendered.
    settings (ResumeCertificationsSettings): Configuration settings that determine which fields to display for each certification.

Notes:
    1. Calls the parent class constructor to initialize common attributes.

---
## method: `RenderCertificationsSection.render(self: UnknownType) -> None`

Render the certifications section in the document.

Args:
    None: This method does not accept any arguments.

Returns:
    None: This method does not return any value.

Notes:
    1. If there are certifications to render, adds a level-2 heading titled "Certifications".
    2. Iterates through each certification in the collection.
    3. For each certification, creates a RenderCertificationSection instance and renders it into the document.

---

===

===
# File: `skills_matrix_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> UnknownType`

Initialize skills render object.

Args:
    document (docx.document.Document): The Word document to render into.
    experience (Experience): The parsed experience data containing roles and skill history.
    settings (ResumeSkillsMatrixSettings): Configuration settings for rendering skills matrix.
    parse_context (ParseContext): Contextual information used during parsing, used to track state.

Returns:
    None

Notes:
    1. Validate that the provided parse_context is an instance of ParseContext.
    2. Store the parse_context for later use during rendering.
    3. Call the parent class constructor with the provided document, experience, and settings.

---

## function: `render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object contains any roles; if not, raise a ValueError.
    2. Create a SkillsMatrix instance from the experience roles.
    3. If settings.all_skills is True, generate a matrix containing all skills; otherwise, use only the specified skills from settings.skills.
    4. Determine the number of rows needed in the table based on the number of skills (with two skills per row).
    5. Add a table with the calculated number of rows and 4 columns, using the "Table Grid" style.
    6. Add a header row with bolded column labels: "Skill", "YOE (from - to)", "Skill", and "YOE (from - to)".
    7. Iterate through the sorted skills and their associated data.
    8. For each skill, place it in the appropriate cell (alternating between columns 0 and 2).
    9. Format the years of experience (YOE) string as "{yoe} ({first_used} - {last_used})", using "N/A" if dates are missing.
    10. Place the formatted YOE string in the corresponding cell to the right of the skill.
    11. Set vertical center alignment for both skill and YOE cells.
    12. Automatically adjust table column widths to fit content.

---

## `RenderSkillsMatrixSection` class

Render skills for a functional resume.

---
## method: `RenderSkillsMatrixSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings, parse_context: ParseContext) -> UnknownType`

Initialize skills render object.

Args:
    document (docx.document.Document): The Word document to render into.
    experience (Experience): The parsed experience data containing roles and skill history.
    settings (ResumeSkillsMatrixSettings): Configuration settings for rendering skills matrix.
    parse_context (ParseContext): Contextual information used during parsing, used to track state.

Returns:
    None

Notes:
    1. Validate that the provided parse_context is an instance of ParseContext.
    2. Store the parse_context for later use during rendering.
    3. Call the parent class constructor with the provided document, experience, and settings.

---
## method: `RenderSkillsMatrixSection.render(self: UnknownType) -> None`

Render skills section for functional resume.

Args:
    None

Returns:
    None

Notes:
    1. Check if the experience object contains any roles; if not, raise a ValueError.
    2. Create a SkillsMatrix instance from the experience roles.
    3. If settings.all_skills is True, generate a matrix containing all skills; otherwise, use only the specified skills from settings.skills.
    4. Determine the number of rows needed in the table based on the number of skills (with two skills per row).
    5. Add a table with the calculated number of rows and 4 columns, using the "Table Grid" style.
    6. Add a header row with bolded column labels: "Skill", "YOE (from - to)", "Skill", and "YOE (from - to)".
    7. Iterate through the sorted skills and their associated data.
    8. For each skill, place it in the appropriate cell (alternating between columns 0 and 2).
    9. Format the years of experience (YOE) string as "{yoe} ({first_used} - {last_used})", using "N/A" if dates are missing.
    10. Place the formatted YOE string in the corresponding cell to the right of the skill.
    11. Set vertical center alignment for both skill and YOE cells.
    12. Automatically adjust table column widths to fit content.

---

===

===
# File: `__init__.py`


===

===
# File: `personal_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The Docx document object to render into.
    personal: The Personal model containing personal information.
    settings: The ResumePersonalSettings object controlling which sections to render.

Returns:
    None.

Notes:
    1. Logs the initialization of the personal basic render object.
    2. Calls the parent class constructor with the provided arguments.

---

## function: `_contact_info(self: UnknownType) -> None`

Render the contact info section.

Args:
    None.

Returns:
    None.

Notes:
    1. Creates a new paragraph in the document.
    2. Extracts contact info from the personal model.
    3. If name is present and enabled in settings, adds the name as a bold, larger font run and adds a line break.
    4. If email is present and enabled in settings, adds the email as a run and adds a line break.
    5. If phone is present and enabled in settings, adds the phone as a run and adds a line break.
    6. If location is present and enabled in settings, adds the location as a run and adds a line break.

---

## function: `_banner(self: UnknownType) -> None`

Render the banner section.

Args:
    None.

Returns:
    None.

Notes:
    1. Extracts the banner text from the personal model.
    2. If banner text is present, adds a level 3 heading "Banner".
    3. Adds the banner text as a paragraph.

---

## function: `_note(self: UnknownType) -> None`

Render the note section.

Args:
    None.

Returns:
    None.

Notes:
    1. Extracts the note text from the personal model.
    2. If note text is present, adds a level 3 heading "Note".
    3. Adds the note text as a paragraph.

---

## function: `_websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initializes an empty list to store website lines.
    2. Extracts websites from the personal model.
    3. If GitHub is present and enabled in settings, appends "GitHub: <url>" to the list.
    4. If LinkedIn is present and enabled in settings, appends "LinkedIn: <url>" to the list.
    5. If website is present and enabled in settings, appends "Website: <url>" to the list.
    6. If Twitter is present and enabled in settings, appends "Twitter: <url>" to the list.
    7. If the list is not empty, adds a level 3 heading "Websites".
    8. Joins the list with newlines and adds it as a paragraph.

---

## function: `_visa_status(self: UnknownType) -> None`

Render the visa status section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initializes an empty list to store visa status lines.
    2. Extracts visa status from the personal model.
    3. If work authorization is present and enabled in settings, appends "Work Authorization: <value>" to the list.
    4. If require_sponsorship is not None and enabled in settings, appends "Require Sponsorship: Yes" or "No" based on the value.
    5. If the list is not empty, adds a level 3 heading "Visa Status".
    6. Joins the list with newlines and adds it as a paragraph.

---

## function: `render(self: UnknownType) -> None`

Render the personal section.

Args:
    None.

Returns:
    None.

Notes:
    1. If contact info exists and enabled in settings, calls _contact_info.
    2. If banner exists and enabled in settings, calls _banner.
    3. If note exists and enabled in settings, calls _note.
    4. If websites exist and enabled in settings, calls _websites.
    5. If visa status exists and enabled in settings, calls _visa_status.

---

## `RenderPersonalSection` class

Render personal contact info section.

---
## method: `RenderPersonalSection.__init__(self: UnknownType, document: docx.document.Document, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The Docx document object to render into.
    personal: The Personal model containing personal information.
    settings: The ResumePersonalSettings object controlling which sections to render.

Returns:
    None.

Notes:
    1. Logs the initialization of the personal basic render object.
    2. Calls the parent class constructor with the provided arguments.

---
## method: `RenderPersonalSection._contact_info(self: UnknownType) -> None`

Render the contact info section.

Args:
    None.

Returns:
    None.

Notes:
    1. Creates a new paragraph in the document.
    2. Extracts contact info from the personal model.
    3. If name is present and enabled in settings, adds the name as a bold, larger font run and adds a line break.
    4. If email is present and enabled in settings, adds the email as a run and adds a line break.
    5. If phone is present and enabled in settings, adds the phone as a run and adds a line break.
    6. If location is present and enabled in settings, adds the location as a run and adds a line break.

---
## method: `RenderPersonalSection._banner(self: UnknownType) -> None`

Render the banner section.

Args:
    None.

Returns:
    None.

Notes:
    1. Extracts the banner text from the personal model.
    2. If banner text is present, adds a level 3 heading "Banner".
    3. Adds the banner text as a paragraph.

---
## method: `RenderPersonalSection._note(self: UnknownType) -> None`

Render the note section.

Args:
    None.

Returns:
    None.

Notes:
    1. Extracts the note text from the personal model.
    2. If note text is present, adds a level 3 heading "Note".
    3. Adds the note text as a paragraph.

---
## method: `RenderPersonalSection._websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initializes an empty list to store website lines.
    2. Extracts websites from the personal model.
    3. If GitHub is present and enabled in settings, appends "GitHub: <url>" to the list.
    4. If LinkedIn is present and enabled in settings, appends "LinkedIn: <url>" to the list.
    5. If website is present and enabled in settings, appends "Website: <url>" to the list.
    6. If Twitter is present and enabled in settings, appends "Twitter: <url>" to the list.
    7. If the list is not empty, adds a level 3 heading "Websites".
    8. Joins the list with newlines and adds it as a paragraph.

---
## method: `RenderPersonalSection._visa_status(self: UnknownType) -> None`

Render the visa status section.

Args:
    None.

Returns:
    None.

Notes:
    1. Initializes an empty list to store visa status lines.
    2. Extracts visa status from the personal model.
    3. If work authorization is present and enabled in settings, appends "Work Authorization: <value>" to the list.
    4. If require_sponsorship is not None and enabled in settings, appends "Require Sponsorship: Yes" or "No" based on the value.
    5. If the list is not empty, adds a level 3 heading "Visa Status".
    6. Joins the list with newlines and adds it as a paragraph.

---
## method: `RenderPersonalSection.render(self: UnknownType) -> None`

Render the personal section.

Args:
    None.

Returns:
    None.

Notes:
    1. If contact info exists and enabled in settings, calls _contact_info.
    2. If banner exists and enabled in settings, calls _banner.
    3. If note exists and enabled in settings, calls _note.
    4. If websites exist and enabled in settings, calls _websites.
    5. If visa status exists and enabled in settings, calls _visa_status.

---

===

===
# File: `certifications_section.py`

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

---

## function: `render(self: UnknownType) -> None`

Render the certifications section.

---

## `RenderCertificationsSection` class

Render Certifications Section.

---
## method: `RenderCertificationsSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

---
## method: `RenderCertificationsSection.render(self: UnknownType) -> None`

Render the certifications section.

---

===

===
# File: `__init__.py`

## function: `render_resume_to_html(resume_data: Resume, template_path: str, output_path: str) -> None`

Renders a resume object to an HTML file using a specified template.

Args:
    resume_data (Resume): The resume object containing all the personal, professional, and
                          other relevant resume details to be rendered.
    template_path (str): The file path to the HTML template used for rendering the resume.
                         This template should contain placeholders for dynamic content.
    output_path (str): The file path where the generated HTML resume will be saved.

Returns:
    None: This function does not return a value; it writes the rendered HTML to the specified file.

Notes:
    1. Loads the HTML template from the file specified by `template_path`.
    2. Parses the `resume_data` structure to extract relevant fields such as name, contact info,
       work experience, education, skills, etc.
    3. Replaces placeholders in the template with actual resume content using a templating engine
       (e.g., Jinja2 or similar).
    4. Saves the rendered HTML to the file specified by `output_path`.
    5. The function performs disk I/O operations to read the template and write the output file.
    6. The function assumes that the template file is valid and contains the expected placeholders.

---


===

===
# File: `resume_main.py`

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The HTML document to render into.
    jinja_env: The Jinja2 environment used for templating.
    resume: The resume data to render.
    settings: The rendering settings for the resume.

Notes:
    1. Calls the parent constructor with the provided arguments.

---

## function: `render(self: UnknownType) -> None`

Render the resume by processing each section.

Args:
    None

Returns:
    None

Notes:
    1. If the resume has personal information and personal rendering is enabled, render the personal section.
    2. If the resume has education data and education rendering is enabled, render the education section.
    3. If the resume has certifications and certifications rendering is enabled, render the certifications section.
    4. If the resume has experience data and experience rendering is enabled, render the experience section.
    5. No disk, network, or database access occurs during this process.

---

## `RenderResume` class

Render a resume in basic format.

---
## method: `RenderResume.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The HTML document to render into.
    jinja_env: The Jinja2 environment used for templating.
    resume: The resume data to render.
    settings: The rendering settings for the resume.

Notes:
    1. Calls the parent constructor with the provided arguments.

---
## method: `RenderResume.render(self: UnknownType) -> None`

Render the resume by processing each section.

Args:
    None

Returns:
    None

Notes:
    1. If the resume has personal information and personal rendering is enabled, render the personal section.
    2. If the resume has education data and education rendering is enabled, render the education section.
    3. If the resume has certifications and certifications rendering is enabled, render the certifications section.
    4. If the resume has experience data and experience rendering is enabled, render the experience section.
    5. No disk, network, or database access occurs during this process.

---

===

===
# File: `skills_matrix_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings) -> UnknownType`

Initialize skills render object.

Args:
    document: The Word document object to which the skills section will be added.
    experience: The experience data containing roles and associated skills.
    settings: Configuration settings for rendering the skills matrix, including
              which skills to include and whether to include all skills.

Notes:
    1. Initializes the base class with the provided document, experience, and settings.
    2. Logs the initialization process.

---

## function: `find_skill_date_range(self: UnknownType, skill: str) -> tuple[datetime | None, datetime | None]`

Find the earliest start date and latest end date for a given skill across roles.

Args:
    skill: The name of the skill to search for in roles.

Returns:
    A tuple containing:
        - The earliest start date for any role that includes the skill (or None if not found).
        - The latest end date for any role that includes the skill (or None if not found).

Notes:
    1. Collects all start dates from roles where the skill appears.
    2. Collects all end dates from roles where the skill appears.
    3. If any roles contain the skill, finds the minimum start date and maximum end date.
    4. Returns the earliest start date and latest end date as a tuple.

---

## function: `_get_skills_matrix(self: UnknownType) -> dict[str, float]`

Compute and filter skills matrix based on settings.

Returns:
    A dictionary mapping skill names to years of experience (float), sorted in descending order.

Notes:
    1. Retrieves all roles from the experience object.
    2. Filters the skills specified in the settings, removing any blank entries.
    3. Creates a SkillsMatrix object from the roles and computes the experience for each skill.
    4. Filters the skills to include only those present in the settings, unless all_skills is True.
    5. Sorts the resulting dictionary by years of experience in descending order.
    6. Returns the filtered and sorted dictionary.

---

## function: `render(self: UnknownType) -> None`

Render the skills matrix section in the document.

Notes:
    1. Validates that the experience object contains at least one role.
    2. Retrieves the filtered skills matrix with years of experience.
    3. Ensures the returned skills dictionary is valid and properly typed.
    4. Calculates the number of rows needed for the table based on the number of skills.
    5. Creates a 4-column table with the calculated number of rows.
    6. Sets a fixed height for each row.
    7. Populates the first two columns with skill names and years of experience (including date range).
    8. Populates the last two columns with the remaining skills and their experience (including date range).
    9. Enables automatic fitting of the table to its content.

---

## `RenderSkillsMatrixSection` class

Render skills for a functional resume.

---
## method: `RenderSkillsMatrixSection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeSkillsMatrixSettings) -> UnknownType`

Initialize skills render object.

Args:
    document: The Word document object to which the skills section will be added.
    experience: The experience data containing roles and associated skills.
    settings: Configuration settings for rendering the skills matrix, including
              which skills to include and whether to include all skills.

Notes:
    1. Initializes the base class with the provided document, experience, and settings.
    2. Logs the initialization process.

---
## method: `RenderSkillsMatrixSection.find_skill_date_range(self: UnknownType, skill: str) -> tuple[datetime | None, datetime | None]`

Find the earliest start date and latest end date for a given skill across roles.

Args:
    skill: The name of the skill to search for in roles.

Returns:
    A tuple containing:
        - The earliest start date for any role that includes the skill (or None if not found).
        - The latest end date for any role that includes the skill (or None if not found).

Notes:
    1. Collects all start dates from roles where the skill appears.
    2. Collects all end dates from roles where the skill appears.
    3. If any roles contain the skill, finds the minimum start date and maximum end date.
    4. Returns the earliest start date and latest end date as a tuple.

---
## method: `RenderSkillsMatrixSection._get_skills_matrix(self: UnknownType) -> dict[str, float]`

Compute and filter skills matrix based on settings.

Returns:
    A dictionary mapping skill names to years of experience (float), sorted in descending order.

Notes:
    1. Retrieves all roles from the experience object.
    2. Filters the skills specified in the settings, removing any blank entries.
    3. Creates a SkillsMatrix object from the roles and computes the experience for each skill.
    4. Filters the skills to include only those present in the settings, unless all_skills is True.
    5. Sorts the resulting dictionary by years of experience in descending order.
    6. Returns the filtered and sorted dictionary.

---
## method: `RenderSkillsMatrixSection.render(self: UnknownType) -> None`

Render the skills matrix section in the document.

Notes:
    1. Validates that the experience object contains at least one role.
    2. Retrieves the filtered skills matrix with years of experience.
    3. Ensures the returned skills dictionary is valid and properly typed.
    4. Calculates the number of rows needed for the table based on the number of skills.
    5. Creates a 4-column table with the calculated number of rows.
    6. Sets a fixed height for each row.
    7. Populates the first two columns with skill names and years of experience (including date range).
    8. Populates the last two columns with the remaining skills and their experience (including date range).
    9. Enables automatic fitting of the table to its content.

---

===

===
# File: `experience_section.py`

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

---

## function: `render(self: UnknownType) -> None`

Render roles section.

Renders the job roles section into the HTML document using a Jinja2 template.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Checks if `self.roles` is empty; if so, logs a debug message and exits.
    2. Logs a debug message indicating rendering has started.
    3. Renders the Jinja2 template with `settings` and `roles` as context.
    4. Adds the rendered string to the document using `add_text`.
    5. No disk, network, or database access is used.

---

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

---

## function: `render(self: UnknownType) -> None`

Render projects section.

Renders the projects section into the HTML document using a Jinja2 template.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Checks if `len(self.projects)` is zero; if so, logs a debug message and returns.
    2. Logs a debug message indicating rendering has started.
    3. Renders the Jinja2 template with `settings` and `projects` as context.
    4. Adds the rendered string to the document using `add_text`.
    5. No disk, network, or database access is used.

---

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

---

## function: `render(self: UnknownType) -> None`

Render experience section.

Renders the experience section into the HTML document, including roles and projects.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Calculates the total number of roles and projects that will be rendered.
    2. If no roles or projects exist, returns early.
    3. Adds an HTML heading "Experience" to the document.
    4. If roles are enabled and roles exist, creates and renders a `RenderRolesSection`.
    5. If projects are enabled and projects exist, creates and renders a `RenderProjectsSection`.
    6. No disk, network, or database access is used.

---

## `RenderRolesSection` class

Render experience roles section.

This class is responsible for rendering a section of job roles within a resume
using a Jinja2 template. It processes role data and outputs formatted HTML.

Args:
    document (HtmlDoc): The HTML document object to which rendered content will be added.
    jinja_env (Environment): The Jinja2 environment used to render templates.
    roles (Roles): A collection of job roles to be rendered.
    settings (ResumeRolesSettings): Configuration settings for how roles should be rendered.

Attributes:
    document (HtmlDoc): The HTML document where output will be added.
    jinja_env (Environment): Jinja2 environment for template rendering.
    roles (Roles): List of roles to render.
    template_name (str): Name of the Jinja2 template file for rendering roles.
    settings (ResumeRolesSettings): Rendering configuration for roles.

Notes:
    1. Initializes the parent class with the provided document, Jinja2 environment,
       roles, template name, and settings.
    2. The `render` method checks if roles exist.
    3. If roles exist, it uses the Jinja2 template to render the roles with the given settings.
    4. The rendered content is added to the document using `add_text`.
    5. No disk, network, or database access is performed.

Returns:
    None

---
## method: `RenderRolesSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

---
## method: `RenderRolesSection.render(self: UnknownType) -> None`

Render roles section.

Renders the job roles section into the HTML document using a Jinja2 template.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Checks if `self.roles` is empty; if so, logs a debug message and exits.
    2. Logs a debug message indicating rendering has started.
    3. Renders the Jinja2 template with `settings` and `roles` as context.
    4. Adds the rendered string to the document using `add_text`.
    5. No disk, network, or database access is used.

---
## `RenderProjectsSection` class

Render experience projects section.

This class renders a section of projects associated with a resume using a Jinja2 template.

Args:
    document (HtmlDoc): The HTML document object to which rendered content will be added.
    jinja_env (Environment): The Jinja2 environment used to render templates.
    projects (Projects): A collection of projects to be rendered.
    settings (ResumeProjectsSettings): Configuration settings for how projects should be rendered.

Attributes:
    document (HtmlDoc): The HTML document where output will be added.
    jinja_env (Environment): Jinja2 environment for template rendering.
    projects (Projects): List of projects to render.
    template_name (str): Name of the Jinja2 template file for rendering projects.
    settings (ResumeProjectsSettings): Rendering configuration for projects.

Notes:
    1. Initializes the parent class with the provided document, Jinja2 environment,
       projects, template name, and settings.
    2. The `render` method checks if projects exist.
    3. If projects exist, it uses the Jinja2 template to render the projects with the given settings.
    4. The rendered content is added to the document using `add_text`.
    5. No disk, network, or database access is performed.

Returns:
    None

---
## method: `RenderProjectsSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

---
## method: `RenderProjectsSection.render(self: UnknownType) -> None`

Render projects section.

Renders the projects section into the HTML document using a Jinja2 template.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Checks if `len(self.projects)` is zero; if so, logs a debug message and returns.
    2. Logs a debug message indicating rendering has started.
    3. Renders the Jinja2 template with `settings` and `projects` as context.
    4. Adds the rendered string to the document using `add_text`.
    5. No disk, network, or database access is used.

---
## `RenderExperienceSection` class

Render experience section.

This class is responsible for rendering the entire experience section of a resume,
including roles and projects, using a Jinja2 template. It aggregates data from
`Experience`, and uses separate renderers for roles and projects.

Args:
    document (HtmlDoc): The HTML document object to which rendered content will be added.
    jinja_env (Environment): The Jinja2 environment used to render templates.
    experience (Experience): The experience data (roles and projects) to be rendered.
    settings (ResumeExperienceSettings): Configuration settings for how experience should be rendered.

Attributes:
    document (HtmlDoc): The HTML document where output will be added.
    jinja_env (Environment): Jinja2 environment for template rendering.
    experience (Experience): The experience data (roles and projects).
    settings (ResumeExperienceSettings): Rendering configuration for experience.

Notes:
    1. Initializes the parent class with the provided document, Jinja2 environment,
       experience, and settings.
    2. Calculates the total number of items (roles + projects) to render.
    3. If no items are present, exits early.
    4. Adds an HTML heading "Experience" to the document.
    5. If roles are enabled in settings and `experience.roles` is not empty,
       creates and renders a `RenderRolesSection`.
    6. If projects are enabled in settings and `experience.projects` is not empty,
       creates and renders a `RenderProjectsSection`.
    7. No disk, network, or database access is performed.

Returns:
    None

---
## method: `RenderExperienceSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

---
## method: `RenderExperienceSection.render(self: UnknownType) -> None`

Render experience section.

Renders the experience section into the HTML document, including roles and projects.

Args:
    None

Returns:
    None: The method adds rendered HTML directly to the document.

Notes:
    1. Calculates the total number of roles and projects that will be rendered.
    2. If no roles or projects exist, returns early.
    3. Adds an HTML heading "Experience" to the document.
    4. If roles are enabled and roles exist, creates and renders a `RenderRolesSection`.
    5. If projects are enabled and projects exist, creates and renders a `RenderProjectsSection`.
    6. No disk, network, or database access is used.

---

===

===
# File: `executive_summary_section.py`

## function: `__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize executive summary render object.

Args:
    document: The Word document object to render into.
    experience: The experience data to render, containing roles and their details.
    settings: The rendering settings that control which categories are included and how they are formatted.

Returns:
    None

Notes:
    1. Logs a debug message indicating initialization.
    2. Calls the parent class constructor to initialize base rendering functionality.

---

## function: `render(self: UnknownType) -> None`

Render the executive summary section of the resume.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Checks if the experience object contains any roles; if not, raises a ValueError.
    3. Extracts unique job categories from the roles in the experience data.
    4. Iterates over the job categories specified in the settings.
    5. For each category, filters roles that belong to that category.
    6. If no roles are found for a category, logs a warning and skips to the next category.
    7. Adds a heading for the current job category to the document with level 4.
    8. For each role in the category:
       a. Checks if a summary is available; if not, logs a warning and skips.
       b. Checks if a company name is available; if not, logs a warning and skips.
       c. Creates a new paragraph with a bullet point style.
       d. Adds the role summary as plain text.
       e. Adds the company name in italics, appended to the summary.
    9. No network, disk, or database access occurs during execution.

---

## `RenderExecutiveSummarySection` class

Render experience for a functional resume.

---
## method: `RenderExecutiveSummarySection.__init__(self: UnknownType, document: docx.document.Document, experience: Experience, settings: ResumeExecutiveSummarySettings) -> None`

Initialize executive summary render object.

Args:
    document: The Word document object to render into.
    experience: The experience data to render, containing roles and their details.
    settings: The rendering settings that control which categories are included and how they are formatted.

Returns:
    None

Notes:
    1. Logs a debug message indicating initialization.
    2. Calls the parent class constructor to initialize base rendering functionality.

---
## method: `RenderExecutiveSummarySection.render(self: UnknownType) -> None`

Render the executive summary section of the resume.

Args:
    None

Returns:
    None

Notes:
    1. Logs a debug message indicating the start of rendering.
    2. Checks if the experience object contains any roles; if not, raises a ValueError.
    3. Extracts unique job categories from the roles in the experience data.
    4. Iterates over the job categories specified in the settings.
    5. For each category, filters roles that belong to that category.
    6. If no roles are found for a category, logs a warning and skips to the next category.
    7. Adds a heading for the current job category to the document with level 4.
    8. For each role in the category:
       a. Checks if a summary is available; if not, logs a warning and skips.
       b. Checks if a company name is available; if not, logs a warning and skips.
       c. Creates a new paragraph with a bullet point style.
       d. Adds the role summary as plain text.
       e. Adds the company name in italics, appended to the summary.
    9. No network, disk, or database access occurs during execution.

---

===

===
# File: `personal_section.py`

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The HTML document to which the rendered personal section will be added.
    jinja_env: The Jinja2 environment used to render the template.
    personal: The personal information object containing contact details.
    settings: The settings object that controls the rendering behavior of the personal section.

Notes:
    1. Logs a debug message indicating the initialization of the personal section renderer.
    2. Calls the parent class's __init__ method with the provided arguments to set up the base renderer.

---

## function: `render(self: UnknownType) -> None`

Render the personal section into the HTML document.

Args:
    None

Returns:
    None

Notes:
    1. Renders the Jinja2 template using the settings and personal data.
    2. Adds the rendered HTML content to the document.
    3. No network, disk, or database access is performed.

---

## `RenderPersonalSection` class

Render personal contact info section.

---
## method: `RenderPersonalSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The HTML document to which the rendered personal section will be added.
    jinja_env: The Jinja2 environment used to render the template.
    personal: The personal information object containing contact details.
    settings: The settings object that controls the rendering behavior of the personal section.

Notes:
    1. Logs a debug message indicating the initialization of the personal section renderer.
    2. Calls the parent class's __init__ method with the provided arguments to set up the base renderer.

---
## method: `RenderPersonalSection.render(self: UnknownType) -> None`

Render the personal section into the HTML document.

Args:
    None

Returns:
    None

Notes:
    1. Renders the Jinja2 template using the settings and personal data.
    2. Adds the rendered HTML content to the document.
    3. No network, disk, or database access is performed.

---

===

===
# File: `education_section.py`

## function: `__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

---

## function: `render(self: UnknownType) -> None`

Render the education section.

---

## `RenderEducationSection` class

Render Education Section.

---
## method: `RenderEducationSection.__init__(self: UnknownType, document: HtmlDoc, jinja_env: Environment, education: Education, settings: ResumeEducationSettings) -> UnknownType`

Initialize the basic education renderer.

---
## method: `RenderEducationSection.render(self: UnknownType) -> None`

Render the education section.

---

===

===
# File: `certifications_section.py`

## function: `__init__(self: UnknownType, document: MarkdownDoc, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The MarkdownDoc instance to which the rendered content will be added.
    certifications: The Certifications object containing the list of certifications to render.
    settings: The ResumeCertificationsSettings object that controls what information to include in the output.

Returns:
    None

Notes:
    1. Validate that the document is an instance of MarkdownDoc.
    2. Validate that the certifications is an instance of Certifications.
    3. Validate that the settings is an instance of ResumeCertificationsSettings.
    4. Call the parent class constructor with the provided arguments.

---

## function: `render_certification(self: UnknownType, certification: Certification) -> None`

Render a single certification in the document.

Args:
    certification: The Certification object containing the details of a single certification to render.

Returns:
    None

Notes:
    1. Extract references to the document and settings for convenience.
    2. Add a header for the certification section.
    3. If the settings require the issuer and the certification has an issuer, add the issuer to the document.
    4. If the settings require the name and the certification has a name, add the name to the document.
    5. If the settings require the issued date and the certification has an issued date, add the issued date to the document.
    6. If the settings require the expiration date and the certification has an expiration date, add the expiration date to the document.
    7. If the settings require the certification ID and the certification has a certification ID, add the certification ID to the document.

---

## function: `render(self: UnknownType) -> None`

Render the certifications section into the document.

Args:
    None

Returns:
    None

Notes:
    1. Extract references to the document and certifications for convenience.
    2. If there are no certifications, log a debug message and return early.
    3. Log a debug message indicating that rendering has started.
    4. Add a top-level header for the certifications section.
    5. Iterate over each certification in the certifications list.
    6. For each certification, call the render_certification method to render its details.

---

## `RenderCertificationsSection` class

Render Certifications Section.

---
## method: `RenderCertificationsSection.__init__(self: UnknownType, document: MarkdownDoc, certifications: Certifications, settings: ResumeCertificationsSettings) -> UnknownType`

Initialize the basic certifications renderer.

Args:
    document: The MarkdownDoc instance to which the rendered content will be added.
    certifications: The Certifications object containing the list of certifications to render.
    settings: The ResumeCertificationsSettings object that controls what information to include in the output.

Returns:
    None

Notes:
    1. Validate that the document is an instance of MarkdownDoc.
    2. Validate that the certifications is an instance of Certifications.
    3. Validate that the settings is an instance of ResumeCertificationsSettings.
    4. Call the parent class constructor with the provided arguments.

---
## method: `RenderCertificationsSection.render_certification(self: UnknownType, certification: Certification) -> None`

Render a single certification in the document.

Args:
    certification: The Certification object containing the details of a single certification to render.

Returns:
    None

Notes:
    1. Extract references to the document and settings for convenience.
    2. Add a header for the certification section.
    3. If the settings require the issuer and the certification has an issuer, add the issuer to the document.
    4. If the settings require the name and the certification has a name, add the name to the document.
    5. If the settings require the issued date and the certification has an issued date, add the issued date to the document.
    6. If the settings require the expiration date and the certification has an expiration date, add the expiration date to the document.
    7. If the settings require the certification ID and the certification has a certification ID, add the certification ID to the document.

---
## method: `RenderCertificationsSection.render(self: UnknownType) -> None`

Render the certifications section into the document.

Args:
    None

Returns:
    None

Notes:
    1. Extract references to the document and certifications for convenience.
    2. If there are no certifications, log a debug message and return early.
    3. Log a debug message indicating that rendering has started.
    4. Add a top-level header for the certifications section.
    5. Iterate over each certification in the certifications list.
    6. For each certification, call the render_certification method to render its details.

---

===

===
# File: `resume_main.py`

## function: `__init__(self: UnknownType, document: MarkdownDoc, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The Markdown document to render the resume into.
    resume: The resume data to render.
    settings: The rendering settings for the resume.

Notes:
    1. Calls the parent class constructor to initialize the base renderer.
    2. Stores the provided document, resume, and settings for later use during rendering.

---

## function: `render(self: UnknownType) -> None`

Render the resume.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return anything.

Notes:
    1. Checks if the resume has personal information and if personal section rendering is enabled.
    2. If both conditions are true, renders the personal section.
    3. Checks if the resume has education information and if education section rendering is enabled.
    4. If both conditions are true, renders the education section.
    5. Checks if the resume has certifications and if certifications section rendering is enabled.
    6. If both conditions are true, renders the certifications section.
    7. Checks if the resume has experience information and if experience section rendering is enabled.
    8. If both conditions are true, renders the experience section.
    9. This method performs no disk, network, or database access.

---

## `RenderResume` class

Render a resume in basic format.

---
## method: `RenderResume.__init__(self: UnknownType, document: MarkdownDoc, resume: Resume, settings: ResumeRenderSettings) -> UnknownType`

Initialize basic resume renderer.

Args:
    document: The Markdown document to render the resume into.
    resume: The resume data to render.
    settings: The rendering settings for the resume.

Notes:
    1. Calls the parent class constructor to initialize the base renderer.
    2. Stores the provided document, resume, and settings for later use during rendering.

---
## method: `RenderResume.render(self: UnknownType) -> None`

Render the resume.

Args:
    None: This method does not take any arguments.

Returns:
    None: This method does not return anything.

Notes:
    1. Checks if the resume has personal information and if personal section rendering is enabled.
    2. If both conditions are true, renders the personal section.
    3. Checks if the resume has education information and if education section rendering is enabled.
    4. If both conditions are true, renders the education section.
    5. Checks if the resume has certifications and if certifications section rendering is enabled.
    6. If both conditions are true, renders the certifications section.
    7. Checks if the resume has experience information and if experience section rendering is enabled.
    8. If both conditions are true, renders the experience section.
    9. This method performs no disk, network, or database access.

---

===

===
# File: `personal_section.py`

## function: `__init__(self: UnknownType, document: MarkdownDoc, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The MarkdownDoc instance to write rendered content to.
    personal: The Personal instance containing personal contact information.
    settings: The ResumePersonalSettings instance defining which fields to render.

Returns:
    None

Notes:
    1. Validate that document is an instance of MarkdownDoc.
    2. Validate that personal is an instance of Personal.
    3. Validate that settings is an instance of ResumePersonalSettings.
    4. Call the parent class constructor with provided arguments.

---

## function: `websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. If websites rendering is enabled in settings and personal has websites data, render the section header.
    3. If GitHub URL is enabled in settings and personal has a GitHub URL, add it to the document.
    4. If LinkedIn URL is enabled in settings and personal has a LinkedIn URL, add it to the document.
    5. If Website URL is enabled in settings and personal has a Website URL, add it to the document.
    6. If Twitter URL is enabled in settings and personal has a Twitter URL, add it to the document.

---

## function: `contact_info(self: UnknownType) -> None`

Render the contact information section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. Add the section header for "Contact Information".
    3. If contact info rendering is enabled in settings and personal has contact info data:
        a. If name rendering is enabled and personal has a name, add the name to the document.
        b. If email rendering is enabled and personal has an email, add the email to the document.
        c. If phone rendering is enabled and personal has a phone number, add the phone number to the document.
        d. If location rendering is enabled and personal has a location, add the location to the document.

---

## function: `render(self: UnknownType) -> None`

Render the personal section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. Add the main section header "# Personal".
    3. Render the contact information section.
    4. If visa status rendering is enabled in settings and personal has visa status data:
        a. Add the section header "## Visa Status".
        b. If work authorization rendering is enabled and personal has work authorization data, add it to the document.
        c. If sponsorship requirement rendering is enabled and personal has a sponsorship requirement, add it to the document.
    5. If banner rendering is enabled in settings and personal has a banner with text, add the banner section header and text.
    6. If note rendering is enabled in settings and personal has a note with text, add the note section header and text.

---

## `RenderPersonalSection` class

Render personal contact info section.

---
## method: `RenderPersonalSection.__init__(self: UnknownType, document: MarkdownDoc, personal: Personal, settings: ResumePersonalSettings) -> UnknownType`

Initialize the personal section renderer.

Args:
    document: The MarkdownDoc instance to write rendered content to.
    personal: The Personal instance containing personal contact information.
    settings: The ResumePersonalSettings instance defining which fields to render.

Returns:
    None

Notes:
    1. Validate that document is an instance of MarkdownDoc.
    2. Validate that personal is an instance of Personal.
    3. Validate that settings is an instance of ResumePersonalSettings.
    4. Call the parent class constructor with provided arguments.

---
## method: `RenderPersonalSection.websites(self: UnknownType) -> None`

Render the websites section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. If websites rendering is enabled in settings and personal has websites data, render the section header.
    3. If GitHub URL is enabled in settings and personal has a GitHub URL, add it to the document.
    4. If LinkedIn URL is enabled in settings and personal has a LinkedIn URL, add it to the document.
    5. If Website URL is enabled in settings and personal has a Website URL, add it to the document.
    6. If Twitter URL is enabled in settings and personal has a Twitter URL, add it to the document.

---
## method: `RenderPersonalSection.contact_info(self: UnknownType) -> None`

Render the contact information section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. Add the section header for "Contact Information".
    3. If contact info rendering is enabled in settings and personal has contact info data:
        a. If name rendering is enabled and personal has a name, add the name to the document.
        b. If email rendering is enabled and personal has an email, add the email to the document.
        c. If phone rendering is enabled and personal has a phone number, add the phone number to the document.
        d. If location rendering is enabled and personal has a location, add the location to the document.

---
## method: `RenderPersonalSection.render(self: UnknownType) -> None`

Render the personal section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve references to document, personal, and settings from self.
    2. Add the main section header "# Personal".
    3. Render the contact information section.
    4. If visa status rendering is enabled in settings and personal has visa status data:
        a. Add the section header "## Visa Status".
        b. If work authorization rendering is enabled and personal has work authorization data, add it to the document.
        c. If sponsorship requirement rendering is enabled and personal has a sponsorship requirement, add it to the document.
    5. If banner rendering is enabled in settings and personal has a banner with text, add the banner section header and text.
    6. If note rendering is enabled in settings and personal has a note with text, add the note section header and text.

---

===

===
# File: `__init__.py`

## function: `render_resume_to_markdown(resume_data: Dict[str, Any], output_file: str) -> None`

Renders resume data to a Markdown file.

Args:
    resume_data (Dict[str, Any]): A dictionary containing resume information
        structured according to the resume schema. Expected keys include personal
        details, experiences, education, skills, and other relevant sections.
    output_file (str): The file path where the generated Markdown content will be
        saved. The file will be overwritten if it already exists.

Returns:
    None: This function does not return a value.

Notes:
    1. The function validates that the resume_data dictionary is not empty.
    2. It calls the internal `render_resume` function to process the data into
       Markdown format.
    3. The resulting Markdown string is written to the specified output file.
    4. Disk access is performed to write the output file.

---

## function: `render_resume_from_file(input_file: str, output_file: str) -> None`

Reads resume data from a file and renders it as Markdown.

Args:
    input_file (str): Path to the input file containing resume data in JSON format.
        The file must be readable and contain valid JSON.
    output_file (str): Path to the output file where the rendered Markdown will be saved.
        The file will be overwritten if it already exists.

Returns:
    None: This function does not return a value.

Notes:
    1. The function reads the input file from disk to load the JSON resume data.
    2. It parses the JSON content into a dictionary.
    3. It calls `render_resume_to_markdown` to convert the data into Markdown.
    4. Disk access is performed both to read the input file and to write the output file.

---


===

===
# File: `education_section.py`

## function: `__init__(self: UnknownType, document: MarkdownDoc, education: Education, settings: ResumeEducationSettings) -> None`

Initialize the basic education renderer.

Args:
    document: The MarkdownDoc instance to which rendered content will be added.
    education: The Education object containing degree information to be rendered.
    settings: The ResumeEducationSettings object defining which fields to render.

Returns:
    None

Notes:
    1. Validate that the provided document is an instance of MarkdownDoc.
    2. Validate that the provided education is an instance of Education.
    3. Validate that the provided settings is an instance of ResumeEducationSettings.
    4. Call the parent class constructor with the provided arguments.

---

## function: `render_degree(self: UnknownType, degree: Degree) -> None`

Render a single degree in the education section.

Args:
    degree: The Degree object containing details such as school, degree, major, dates, and GPA.

Returns:
    None

Notes:
    1. Retrieve shortcuts for the document and settings.
    2. Add a header for the degree section with "### Degree".
    3. If the settings flag for school is enabled and the degree has a school, add the school to the document.
    4. If the settings flag for degree is enabled and the degree has a degree name, add the degree to the document.
    5. If the settings flag for major is enabled and the degree has a major, add the major to the document.
    6. If the settings flag for start_date is enabled and the degree has a start date, format and add the start date to the document.
    7. If the settings flag for end_date is enabled and the degree has an end date, format and add the end date to the document.
    8. If the settings flag for gpa is enabled and the degree has a GPA, add the GPA to the document.

---

## function: `render(self: UnknownType) -> None`

Render the complete education section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve shortcuts for the document, settings, and education.
    2. If the settings flag for degrees is disabled, log a debug message and return.
    3. Log a debug message indicating that the education section is being rendered.
    4. Add a top-level header for the education section with "# Education".
    5. Add a sub-header for the degrees section with "## Degrees".
    6. Iterate over each degree in the education object and call render_degree for each.

---

## `RenderEducationSection` class

Render Education Section.

---
## method: `RenderEducationSection.__init__(self: UnknownType, document: MarkdownDoc, education: Education, settings: ResumeEducationSettings) -> None`

Initialize the basic education renderer.

Args:
    document: The MarkdownDoc instance to which rendered content will be added.
    education: The Education object containing degree information to be rendered.
    settings: The ResumeEducationSettings object defining which fields to render.

Returns:
    None

Notes:
    1. Validate that the provided document is an instance of MarkdownDoc.
    2. Validate that the provided education is an instance of Education.
    3. Validate that the provided settings is an instance of ResumeEducationSettings.
    4. Call the parent class constructor with the provided arguments.

---
## method: `RenderEducationSection.render_degree(self: UnknownType, degree: Degree) -> None`

Render a single degree in the education section.

Args:
    degree: The Degree object containing details such as school, degree, major, dates, and GPA.

Returns:
    None

Notes:
    1. Retrieve shortcuts for the document and settings.
    2. Add a header for the degree section with "### Degree".
    3. If the settings flag for school is enabled and the degree has a school, add the school to the document.
    4. If the settings flag for degree is enabled and the degree has a degree name, add the degree to the document.
    5. If the settings flag for major is enabled and the degree has a major, add the major to the document.
    6. If the settings flag for start_date is enabled and the degree has a start date, format and add the start date to the document.
    7. If the settings flag for end_date is enabled and the degree has an end date, format and add the end date to the document.
    8. If the settings flag for gpa is enabled and the degree has a GPA, add the GPA to the document.

---
## method: `RenderEducationSection.render(self: UnknownType) -> None`

Render the complete education section.

Args:
    None

Returns:
    None

Notes:
    1. Retrieve shortcuts for the document, settings, and education.
    2. If the settings flag for degrees is disabled, log a debug message and return.
    3. Log a debug message indicating that the education section is being rendered.
    4. Add a top-level header for the education section with "# Education".
    5. Add a sub-header for the degrees section with "## Degrees".
    6. Iterate over each degree in the education object and call render_degree for each.

---

===

===
# File: `experience_section.py`

## function: `__init__(self: UnknownType, document: MarkdownDoc, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The MarkdownDoc object to render the content into.
    roles: The list of Role objects to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Validate that `document` is an instance of MarkdownDoc.
    2. Validate that `roles` is an instance of Roles.
    3. Validate that `settings` is an instance of ResumeRolesSettings.
    4. Call the parent class constructor with the provided arguments.

---

## function: `render_basics(self: UnknownType, role: Role) -> None`

Render role basics.

Args:
    role: The Role object containing the basic information to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the basics section.
    3. Render the company name if present.
    4. Render the agency name if the setting is enabled and the field is present.
    5. Render the job category if the setting is enabled and the field is present.
    6. Render the employment type if the setting is enabled and the field is present.
    7. Render the start date if the setting is enabled and the field is present.
    8. Render the end date if the setting is enabled and the field is present.
    9. Render the title if present.
    10. Render the reason for change if the setting is enabled and the field is present.
    11. Render the location if the setting is enabled and the field is present.

---

## function: `render_highlights(self: UnknownType, role: Role) -> None`

Render role highlights.

Args:
    role: The Role object containing the highlights to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If highlights are enabled in settings and the role has highlights, add a header for highlights.
    3. For each highlight in the role, add a bullet point to the document.

---

## function: `render_responsibilities(self: UnknownType, role: Role) -> None`

Render role responsibilities.

Args:
    role: The Role object containing the responsibilities to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If responsibilities are enabled in settings and the role has responsibilities, add a header for responsibilities.
    3. For each responsibility in the role, add a bullet point to the document.

---

## function: `render_skills(self: UnknownType, role: Role) -> None`

Render role skills.

Args:
    role: The Role object containing the skills to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If skills are enabled in settings and the role has skills, add a header for skills.
    3. For each skill in the role, add a bullet point to the document.

---

## function: `render_projects(self: UnknownType, role: Role) -> None`

Render role projects.

Args:
    role: The Role object containing the projects to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If projects are enabled in settings and the role has projects, add a header for projects.
    3. For each project in the role, add a bullet point to the document.

---

## function: `render_role(self: UnknownType, role: Role) -> None`

Render a single role.

Args:
    role: The Role object to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the role section.
    3. Render the role basics.
    4. If summary is enabled and the role has a non-empty summary, add a header and render the summary.
    5. If responsibilities are enabled and the role has a text field for responsibilities, add a header and render the text.
    6. If skills are enabled and the role has skills, add a header and render each skill with an asterisk bullet.

---

## function: `render(self: UnknownType) -> None`

Render roles section.

Args:
    None

Returns:
    None

Notes:
    1. Extract shortcuts for the document and roles.
    2. If no roles are present, log a debug message and return.
    3. Log a debug message indicating that rendering is starting.
    4. Add a header for the roles section.
    5. For each role in the roles list, render the role.

---

## function: `__init__(self: UnknownType, document: MarkdownDoc, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The MarkdownDoc object to render the content into.
    projects: The list of Project objects to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Log a debug message indicating initialization.
    2. Validate that `document` is an instance of MarkdownDoc.
    3. Validate that `projects` is an instance of Projects.
    4. Validate that `settings` is an instance of ResumeProjectsSettings.
    5. Call the parent class constructor with the provided arguments.

---

## function: `render_project(self: UnknownType, project: Project) -> None`

Render a single project.

Args:
    project: The Project object to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the project section.
    3. Add a header for the overview section.
    4. Render the project title if enabled in settings and present.
    5. Render the project URL if enabled in settings and present.
    6. Render the URL description if enabled in settings and present.
    7. Render the start date if enabled in settings and present.
    8. Render the end date if enabled in settings and present.
    9. If a description is enabled in settings and present, add a header and render the description.
    10. If skills are enabled in settings and present, add a header and render each skill with an asterisk bullet.

---

## function: `render(self: UnknownType) -> None`

Render projects section.

Args:
    None

Returns:
    None

Notes:
    1. Extract shortcuts for the document, settings, and projects.
    2. If no projects are present, log a debug message and return.
    3. Log a debug message indicating that rendering is starting.
    4. Add a header for the projects section.
    5. For each project in the projects list, render the project.

---

## function: `__init__(self: UnknownType, document: MarkdownDoc, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The MarkdownDoc object to render the content into.
    experience: The Experience object containing the data to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Log a debug message indicating initialization.
    2. Call the parent class constructor with the provided arguments.

---

## function: `render(self: UnknownType) -> None`

Render experience section.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating that rendering is starting.
    2. Add a header for the experience section.
    3. If projects are enabled in settings and the experience has projects, render the projects section.
    4. If roles are enabled in settings and the experience has roles, render the roles section.

---

## `RenderRolesSection` class

Render experience roles section.

---
## method: `RenderRolesSection.__init__(self: UnknownType, document: MarkdownDoc, roles: Roles, settings: ResumeRolesSettings) -> UnknownType`

Initialize roles render object.

Args:
    document: The MarkdownDoc object to render the content into.
    roles: The list of Role objects to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Validate that `document` is an instance of MarkdownDoc.
    2. Validate that `roles` is an instance of Roles.
    3. Validate that `settings` is an instance of ResumeRolesSettings.
    4. Call the parent class constructor with the provided arguments.

---
## method: `RenderRolesSection.render_basics(self: UnknownType, role: Role) -> None`

Render role basics.

Args:
    role: The Role object containing the basic information to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the basics section.
    3. Render the company name if present.
    4. Render the agency name if the setting is enabled and the field is present.
    5. Render the job category if the setting is enabled and the field is present.
    6. Render the employment type if the setting is enabled and the field is present.
    7. Render the start date if the setting is enabled and the field is present.
    8. Render the end date if the setting is enabled and the field is present.
    9. Render the title if present.
    10. Render the reason for change if the setting is enabled and the field is present.
    11. Render the location if the setting is enabled and the field is present.

---
## method: `RenderRolesSection.render_highlights(self: UnknownType, role: Role) -> None`

Render role highlights.

Args:
    role: The Role object containing the highlights to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If highlights are enabled in settings and the role has highlights, add a header for highlights.
    3. For each highlight in the role, add a bullet point to the document.

---
## method: `RenderRolesSection.render_responsibilities(self: UnknownType, role: Role) -> None`

Render role responsibilities.

Args:
    role: The Role object containing the responsibilities to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If responsibilities are enabled in settings and the role has responsibilities, add a header for responsibilities.
    3. For each responsibility in the role, add a bullet point to the document.

---
## method: `RenderRolesSection.render_skills(self: UnknownType, role: Role) -> None`

Render role skills.

Args:
    role: The Role object containing the skills to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If skills are enabled in settings and the role has skills, add a header for skills.
    3. For each skill in the role, add a bullet point to the document.

---
## method: `RenderRolesSection.render_projects(self: UnknownType, role: Role) -> None`

Render role projects.

Args:
    role: The Role object containing the projects to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. If projects are enabled in settings and the role has projects, add a header for projects.
    3. For each project in the role, add a bullet point to the document.

---
## method: `RenderRolesSection.render_role(self: UnknownType, role: Role) -> None`

Render a single role.

Args:
    role: The Role object to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the role section.
    3. Render the role basics.
    4. If summary is enabled and the role has a non-empty summary, add a header and render the summary.
    5. If responsibilities are enabled and the role has a text field for responsibilities, add a header and render the text.
    6. If skills are enabled and the role has skills, add a header and render each skill with an asterisk bullet.

---
## method: `RenderRolesSection.render(self: UnknownType) -> None`

Render roles section.

Args:
    None

Returns:
    None

Notes:
    1. Extract shortcuts for the document and roles.
    2. If no roles are present, log a debug message and return.
    3. Log a debug message indicating that rendering is starting.
    4. Add a header for the roles section.
    5. For each role in the roles list, render the role.

---
## `RenderProjectsSection` class

Render experience projects section.

---
## method: `RenderProjectsSection.__init__(self: UnknownType, document: MarkdownDoc, projects: Projects, settings: ResumeProjectsSettings) -> UnknownType`

Initialize projects render object.

Args:
    document: The MarkdownDoc object to render the content into.
    projects: The list of Project objects to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Log a debug message indicating initialization.
    2. Validate that `document` is an instance of MarkdownDoc.
    3. Validate that `projects` is an instance of Projects.
    4. Validate that `settings` is an instance of ResumeProjectsSettings.
    5. Call the parent class constructor with the provided arguments.

---
## method: `RenderProjectsSection.render_project(self: UnknownType, project: Project) -> None`

Render a single project.

Args:
    project: The Project object to render.

Returns:
    None

Notes:
    1. Extract shortcuts for the document and settings.
    2. Add a header for the project section.
    3. Add a header for the overview section.
    4. Render the project title if enabled in settings and present.
    5. Render the project URL if enabled in settings and present.
    6. Render the URL description if enabled in settings and present.
    7. Render the start date if enabled in settings and present.
    8. Render the end date if enabled in settings and present.
    9. If a description is enabled in settings and present, add a header and render the description.
    10. If skills are enabled in settings and present, add a header and render each skill with an asterisk bullet.

---
## method: `RenderProjectsSection.render(self: UnknownType) -> None`

Render projects section.

Args:
    None

Returns:
    None

Notes:
    1. Extract shortcuts for the document, settings, and projects.
    2. If no projects are present, log a debug message and return.
    3. Log a debug message indicating that rendering is starting.
    4. Add a header for the projects section.
    5. For each project in the projects list, render the project.

---
## `RenderExperienceSection` class

Render experience section.

---
## method: `RenderExperienceSection.__init__(self: UnknownType, document: MarkdownDoc, experience: Experience, settings: ResumeExperienceSettings) -> None`

Initialize experience render object.

Args:
    document: The MarkdownDoc object to render the content into.
    experience: The Experience object containing the data to render.
    settings: The settings object controlling what fields to render.

Returns:
    None

Notes:
    1. Log a debug message indicating initialization.
    2. Call the parent class constructor with the provided arguments.

---
## method: `RenderExperienceSection.render(self: UnknownType) -> None`

Render experience section.

Args:
    None

Returns:
    None

Notes:
    1. Log a debug message indicating that rendering is starting.
    2. Add a header for the experience section.
    3. If projects are enabled in settings and the experience has projects, render the projects section.
    4. If roles are enabled in settings and the experience has roles, render the roles section.

---

===

