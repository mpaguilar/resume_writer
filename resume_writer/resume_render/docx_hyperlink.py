"""Add a hyperlink to a run.

`python-docx` doesn't have a built-in way to add a hyperlink to a run.
According to the documentation, this functionality is in-progress.

Found most of this in a GitHub comment.

"""

import docx
from docx import Document
from docx.text.paragraph import Paragraph


def get_or_create_hyperlink_style(d: Document) -> str:
    """Create a hyperlink style if one doesn't exist, or return existing style.

    Args:
        d (Document): The Document object to check or modify for the hyperlink style.

    Returns:
        str: The name of the style used for hyperlinks, which is "Hyperlink".

    Notes:
        1. Check if a style named "Hyperlink" already exists in the document.
        2. If not, create a new style named "Default Character Font" with default character formatting.
        3. The "Default Character Font" style is set to be the default font and is hidden.
        4. Create a new style named "Hyperlink" based on the "Default Character Font" style.
        5. Set the hyperlink style to be visible when used and apply blue color and underline to the font.
        6. Return the name "Hyperlink" as the style identifier.

    """
    if "Hyperlink" not in d.styles:
        if "Default Character Font" not in d.styles:
            ds = d.styles.add_style(
                "Default Character Font",
                docx.enum.style.WD_STYLE_TYPE.CHARACTER,
                True,  # noqa: FBT003
            )
            ds.element.set(docx.oxml.shared.qn("w:default"), "1")
            ds.priority = 1
            ds.hidden = True
            ds.unhide_when_used = True
            del ds
        hs = d.styles.add_style(
            "Hyperlink",
            docx.enum.style.WD_STYLE_TYPE.CHARACTER,
            True,  # noqa: FBT003
        )
        hs.base_style = d.styles["Default Character Font"]
        hs.unhide_when_used = True
        hs.font.color.rgb = docx.shared.RGBColor(0x05, 0x63, 0xC1)
        hs.font.underline = True
        del hs

    return "Hyperlink"


def add_hyperlink(
    paragraph: Paragraph,
    text: str,
    url: str,
) -> docx.oxml.shared.OxmlElement:
    """Create a hyperlink object and add it to the paragraph.

    Args:
        paragraph (Paragraph): The Paragraph object to which the hyperlink will be added.
        text (str): The text to display as the hyperlink.
        url (str): The URL that the hyperlink will point to.

    Returns:
        docx.oxml.shared.OxmlElement: The OxmlElement representing the hyperlink, which is added to the paragraph.

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

    """
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(
        url,
        docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK,
        is_external=True,
    )

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement("w:hyperlink")
    hyperlink.set(
        docx.oxml.shared.qn("r:id"),
        r_id,
    )

    # Create a new run object (a wrapper over a 'w:r' element)
    new_run = docx.text.run.Run(docx.oxml.shared.OxmlElement("w:r"), paragraph)
    new_run.text = text

    # Set the run's style to the builtin hyperlink style, defining it if necessary
    new_run.style = get_or_create_hyperlink_style(part.document)

    # Join all the xml elements together
    hyperlink.append(new_run._element)  # noqa: SLF001
    paragraph._p.append(hyperlink)  # noqa: SLF001
    return hyperlink
