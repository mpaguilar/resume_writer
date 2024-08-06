import logging
from pathlib import Path

import rich
from docx_render.ats_resume import ATSResume
from docx_render.resume_settings import ResumeSettings
from models.personal import Personal
from models.resume import Resume
from utils.resume_stats import DateStats

log = logging.basicConfig(level=logging.DEBUG)


def print_personal(personal: Personal) -> None:
    """Print the personal information."""
    rich.print(f"[bold]Name:[/bold] {personal.contact_info.name}")
    rich.print(f"[bold]Email:[/bold] {personal.contact_info.email}")
    rich.print(f"[bold]Phone:[/bold] {personal.contact_info.phone}")


def career_years_of_experience(resume: Resume) -> None:
    """Print the years of experience."""
    _roles = resume.roles
    _date_stats = DateStats()
    for role in _roles:
        _date_stats.add_date_range(role.basics.start_date, role.basics.end_date)

    _yoe = _date_stats.years_of_experience

    rich.print(f"[bold]Years of Experience:[/bold] {_yoe}")


def dump_resume(resume: Resume) -> None:
    """Dump the resume to the console."""

    _personal = resume.personal
    print_personal(_personal)
    career_years_of_experience(resume)


def export_ats_document(resume: Resume) -> None:
    """Export the resume to a .docx file."""
    _settings = ResumeSettings()
    _docx = ATSResume(resume, _settings)
    _docx.render(Path("data/resume.docx"))


def go() -> None:
    """Start the app."""

    with open("../tests/test_resume.md") as f:
        _resume_text = f.read()

    _resume_lines = _resume_text.split("\n")
    _resume = Resume.parse(_resume_lines)

    # dump the resume to the console
    dump_resume(_resume)
    export_ats_document(_resume)


if __name__ == "__main__":
    go()
