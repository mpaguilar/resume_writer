import logging
from pathlib import Path

import click
import docx
import rich
import tomli

from resume_writer.models.personal import Personal
from resume_writer.models.resume import Resume
from resume_writer.resume_render.basic.resume_main import (
    RenderResume as BasicRenderResume,
)
from resume_writer.resume_render.functional.resume_main import (
    RenderResume as FunctionalRenderResume,
)
from resume_writer.resume_render.plain.resume_main import (
    RenderResume as PlainRenderResume,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
from resume_writer.resume_render.simple.simple_resume import (
    BasicRenderResume as SimpleRenderResume,
)
from resume_writer.utils.resume_stats import DateStats

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


def load_settings(settings_file: str) -> dict:
    """Load settings from TOML and return a dict."""
    _settings_file = Path(settings_file)

    with _settings_file.open("rb") as _f:
        _toml = tomli.load(_f)
        rich.print(_toml)
    return _toml

def basic_render(
        docx_doc: docx.document.Document,
        resume: Resume,
        settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the basic renderer."""

    assert isinstance(docx_doc, docx.document.Document)
    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering simple resume")
    _renderer = BasicRenderResume(document=docx_doc, resume=resume, settings=settings)
    _renderer.render()
    log.info("Render of simple resume complete")

def simple_render(
    docx_doc: docx.document.Document,
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the simple renderer."""

    assert isinstance(docx_doc, docx.document.Document)
    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering simple resume")
    _renderer = SimpleRenderResume(document=docx_doc, resume=resume, settings=settings)
    _renderer.render()
    log.info("Render of simple resume complete")


def functional_render(
    docx_doc: docx.document.Document,
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the functional renderer."""

    assert isinstance(docx_doc, docx.document.Document)
    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering functional resume")

    _renderer = FunctionalRenderResume(
        document=docx_doc,
        resume=resume,
        settings=settings,
    )
    _renderer.render()

    log.info("Render of functional resume complete")

def plain_render(
    docx_doc: docx.document.Document,
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the plain renderer."""

    assert isinstance(docx_doc, docx.document.Document)
    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering plain resume")

    _renderer = PlainRenderResume(
        document=docx_doc,
        resume=resume,
        settings=settings,
    )
    _renderer.render()

    log.info("Render of plain resume complete")

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-file", type=click.Path(), default="data/resume.docx")
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
    default="resume_settings.toml",
)
@click.option(
    "--resume-type",
    type=click.Choice(["simple", "functional", "basic", "plain"]),
    default="simple",
)
def main(
    input_file: str,
    output_file: str,
    settings_file: str,
    resume_type: str,
) -> None:
    """Convert a text resume to a .docx file."""

    _settings = load_settings(settings_file)
    _render_settings = ResumeRenderSettings()
    _render_settings.update_from_dict(_settings["resume"]["render"])

    with open(input_file) as _f:
        _resume_text = _f.read()
        _resume_lines = _resume_text.splitlines(keepends=True)

    _resume = Resume.parse(_resume_lines)
    _docx_doc = docx.Document()

    if resume_type == "simple":
        simple_render(_docx_doc, _resume, _render_settings)
    elif resume_type == "functional":
        functional_render(_docx_doc, _resume, _render_settings)
    elif resume_type == "basic":
        basic_render(_docx_doc, _resume, _render_settings)
    elif resume_type == "plain":
        plain_render(_docx_doc, _resume, _render_settings)
    else:
        raise ValueError(f"Unknown resume type: {resume_type}")
    _docx_doc.save(output_file)
    log.info(f"Saved resume to {output_file}")

    rich.print(_resume)


if __name__ == "__main__":
    main()
