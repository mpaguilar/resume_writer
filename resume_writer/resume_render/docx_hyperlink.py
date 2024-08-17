"""Add a hyperlink to a run.

`python-docx` doesn't have a built-in way to add a hyperlink to a run.
According to the documentation, this functionality is in-progress.

Found most of this in a GitHub comment.

"""

import docx
from docx import Document
from docx.text.paragraph import Paragraph


def get_or_create_hyperlink_style(d: Document) -> str:
    """Create a hyperlink style if one doesn't exist, or return existing style."""

    """If this document had no hyperlinks so far, the builtin
    Hyperlink style will likely be missing and we need to add it.
    There's no predefined value, different Word versions
    define it differently.
    This version is how Word 2019 defines it in the
    default theme, excluding a theme reference.
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
    """Create a hyperlink object and add it to the paragraph."""

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
