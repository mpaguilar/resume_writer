"""
Plain text resume renderer.

This module provides functionality to render a resume in plain text format.
"""

from typing import Any, Dict, List, Optional

from resume_writer.models.resume import Resume


def render_resume(resume: Resume, output_file: str) -> None:
    """
    Render a resume object to plain text format and save it to a file.

    Args:
        resume (Resume): The resume object containing all resume data.
        output_file (str): The path to the output file where the plain text resume will be saved.

    Returns:
        None: This function does not return a value.

    Notes:
        1. The function retrieves the resume data from the Resume object using the to_dict() method.
        2. It constructs a list of strings representing each line of the plain text resume.
        3. For each key-value pair in the resume data:
            a. If the value is a list, it appends the key followed by a colon to the lines list.
            b. Then, for each item in the list, it appends a line with two spaces of indentation and a dash.
        4. If the value is not a list, it appends a line with the key, a colon, and the value.
        5. The function writes the resulting plain text content to the specified output file.
        6. The function performs disk access to write the plain text content to the output file.
    """
    # Extract resume data
    data = resume.to_dict()

    # Build plain text content
    lines: List[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")

    # Write to file
    with open(output_file, "w") as f:
        f.write("\n".join(lines))
