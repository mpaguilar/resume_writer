# A note about date formats
Updating date parsing is a high priority, but for now, dates should be in the format of `MM/YYYY`. You will receive an error if this format isn't followed.

# Types of sections

There are four types of sections, primary sections, key/value sections, list sections, and text sections. Section types are not mixed, for example, a section is either text or a list, but not both.

## Primary sections
Primary sections contain only other sections. `# Personal` is a primary section, and has no fields of it's own.

There are two kinds of primary sections (technically three, but one of them is also a text field).

### Basic sections
These sections contain sections with different names. For example, the `Personal` section contains `Contact Information`, `Websites` and so on. There is no repitition of section names.

### Repeating sections
These sections contain sections with the same name. For example, the `Education` section contains multiple `Degree` sections.

## Section formatting

### Primary sections
Primary sections have no additional text, only subsections.

```
# Personal
## Contact Information
```

### Key/value sections
Key/value pairs are a field name followed by a colon, and then the value for the field. Keys are not case insenstive, values are output verbatim.

```
## Contact Information
Name: John Doe
Email: johndoe@example.com
```

### List sections
List sections contain lists of items, 1 per line, preceeded with an asterisk ("*").

```
## Skills
* Item 1
* Item 2
```

### Text sections

Text sections contain free-form text. They will be added to the document verbatim.
```
### Description
Plain text goes here.

Multiple lines are fine.
```

## Section details

`# Personal` - Primary section. Input for the heading fields. Subsections include Contact Information, Websites, Visa Status, Banner, and Note.

`## Contact Information` - Key/Value section. Input for the contact information fields. Keys include Name, Email, Phone, and Location.

`## Websites` - Key/Value section. Input for the website fields. Keys include GitHub, LinkedIn, Website, and Twitter.

`## Visa Status` - Key/Value section. Input for work authorization status. Keys include Work Authorization and Require Sponsorship.

`## Banner` - Text section. Input for the banner text, a simple short description of who you are.

`## Note` - Text section. Input for a note to be displayed in smaller text, to call out anything that might otherwise be overlooked.

`# Education` - Primary section. Input for education information. Subsections include repeating Degree sections.

`## Degree` - Key/Value section. Input for a degree. Keys include Degree, School, Start Date, End Date, Major, and GPA.

`# Certifications` - Primary section. Input for certifications. Subsections include repeating Certification sections.

`## Certification` - Key/Value section. Input for a certification. Keys include Name, Issuer, Issued, and Expires.

`# Experience` - Primary section. Input for work experience. Subsections include Projects and Roles.

`## Projects` - Primary section. Input for projects. Subsections include repeating Project sections.

`### Project` - Primary section. Subsections include Overview, Description, and Skills.

`#### Overview` - Key/Value section. Input for project overview. Keys include Title, Url, Url description, Start Date, and End Date.

`#### Description` - Text section. Input for project description.

`#### Skills` - List section. Input for project skills.

`## Roles` - Primary section. Input for roles. Subsections include repeating Role sections.

`### Role` - Primary section. Subsections include Basics, Summary, Responsibilities, and Skills.

`#### Basics` - Key/Value section. Input for role basics. Keys include Company, Agency, Job Category, Employment Type, Start Date, End Date, Title, Reason for Change, and Location.

`#### Summary` - Text section. Input for a short summary.

`#### Responsibilities` - Text section. Input for role responsibilities.

`#### Skills` - List section. Input for role skills.


