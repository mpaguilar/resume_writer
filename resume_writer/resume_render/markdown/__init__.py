"""
This module provides utilities for rendering resume data as Markdown format.

The module includes functions to convert structured resume data into Markdown
syntax, which can be used for documentation, web publishing, or further processing.
"""

from typing import Any, Dict, List, Optional
from .render import render_resume
import json


def render_resume_to_markdown(resume_data: Dict[str, Any], output_file: str) -> None:
    """
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
    """
    if not resume_data:
        raise ValueError("resume_data must not be empty")

    markdown_content = render_resume(resume_data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)


def render_resume_from_file(input_file: str, output_file: str) -> None:
    """
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
    """
    with open(input_file, "r", encoding="utf-8") as f:
        resume_data = json.load(f)

    render_resume_to_markdown(resume_data, output_file)
