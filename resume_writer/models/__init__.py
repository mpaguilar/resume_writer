"""
This module serves as the entry point for the resume writing model components.

It provides a unified interface to access various resume-related data structures and parsing logic.
All classes defined in this module are intended to be used in combination to parse and generate structured resume content.

The module does not contain any functions or methods of its own, but instead imports and exposes types and classes from submodules,
such as personal information, work experience, education, and skills, which are used to build a complete resume.

This module is designed to be used with external parsing logic (e.g., from resume_writer.parsers) to transform raw resume text into structured data.

Classes:
    Personal: Represents personal information such as name, contact details, and summary.
        Attributes:
            name (str): Full name of the individual.
            email (str): Contact email address.
            phone (str): Phone number.
            summary (str): Brief professional summary.
            location (str, optional): Geographic location of the individual.

    Resume: Represents the complete resume structure, including sections like personal info, work experience, education, and skills.
        Attributes:
            personal (Personal): Personal details of the individual.
            work_experience (list[WorkExperience]): List of work experience entries.
            education (list[Education]): List of education entries.
            skills (list[Skill]): List of skills possessed by the individual.

Notes:
    1. This module imports and exposes classes from submodules to simplify access for users.
    2. No file or network I/O occurs during module import.
    3. The module is designed to be used in conjunction with parsing logic (e.g., from resume_writer.parsers) to transform raw resume text into structured data.
"""

# All classes are imported from submodules to expose them here.
# This enables users to import from this module directly instead of navigating into submodules.
from .personal import Personal
from .resume import Resume
