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
        1. The function retrieves the resume data from the Resume object.
        2. It formats the resume data into plain text, using appropriate indentation and spacing.
        3. The formatted text is written to the specified output file.
        4. The function performs disk access to write the plain text content to the output file.
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
