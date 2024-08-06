import logging
from pathlib import Path

import click
import rich
import tomli
from docx_render.ats_resume import ATSResume
from docx_render.resume_settings import ResumeSettings
from models.personal import Personal
from models.resume import Resume
from utils.resume_stats import DateStats

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


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


def resume_settings(settings_file: str) -> ResumeSettings:
    """Load the resume settings."""
    _resume_settings = ResumeSettings()
    _settings_file = Path(settings_file)

    with _settings_file.open("rb") as _f:
        _toml = tomli.load(_f)
        rich.print(_toml)

    _settings = _toml.get("resume")
    if _settings is not None:
        _resume_settings.update(_settings)

    return _resume_settings


def export_ats_document(
    resume: Resume,
    output_file: str,
    resume_settings: ResumeSettings,
) -> None:
    """Export the resume to a .docx file."""

    assert isinstance(resume, Resume)
    assert isinstance(output_file, str)
    assert isinstance(resume_settings, ResumeSettings)

    _docx = ATSResume(resume, resume_settings)
    _docx.render(Path(output_file))


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-file", type=click.Path(), default="data/resume.docx")
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
    default="resume_settings.toml",
)
@click.option("--qtest", is_flag=True, default=False)
def main(input_file: str, output_file: str, settings_file: str, qtest: bool) -> None:  # noqa: FBT001
    """Convert a text resume to a .docx file."""

    _settings = resume_settings(settings_file)
    if qtest:
        log.warning("Returning early")
        return

    with open(input_file) as _f:
        _resume_text = _f.read()

    _resume_lines = _resume_text.split("\n")
    _resume = Resume.parse(_resume_lines)
    export_ats_document(_resume, output_file, _settings)


if __name__ == "__main__":
    main()
