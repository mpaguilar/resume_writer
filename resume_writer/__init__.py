"""
Main module for the resume writer package.

This module serves as the entry point for the resume writing functionality.
It provides access to core components such as parsers, models, and processing utilities.

Classes:
    - ResumeParser: Parses resume content from various formats.
    - ResumeModel: Represents a resume with structured data.
    - ResumeWriter: Generates resumes from parsed data.

Functions:
    - parse_resume(file_path: str) -> ResumeModel: Parses a resume file and returns a structured model.
    - write_resume(resume_model: ResumeModel, output_path: str) -> None: Writes a resume model to a file.
"""

from .models.parsers import ResumeParser
from .models.resume import ResumeModel
from .writers.writer import ResumeWriter

__all__ = ['ResumeParser', 'ResumeModel', 'ResumeWriter']

def parse_resume(file_path: str) -> ResumeModel:
    """Parse a resume file and return a structured model.

    Args:
        file_path (str): The path to the resume file (e.g., .txt, .pdf, .docx).

    Returns:
        ResumeModel: A structured model representing the parsed resume data.

    Notes:
        1. The function validates the file path and checks if the file exists.
        2. It uses the ResumeParser to parse the file content.
        3. The parsed data is converted into a ResumeModel instance.
        4. The function handles file format detection and delegates parsing accordingly.
        5. Disk access is performed to read the file from the provided path.
    """

def write_resume(resume_model: ResumeModel, output_path: str) -> None:
    """Write a resume model to a file.

    Args:
        resume_model (ResumeModel): The resume model to write.
        output_path (str): The path where the resume file will be saved.

    Returns:
        None

    Notes:
        1. The function validates the output path and ensures the directory exists.
        2. It uses the ResumeWriter to generate the resume file.
        3. The resume model is serialized and written to the specified output path.
        4. Disk access is performed to save the file to the provided path.
    """
