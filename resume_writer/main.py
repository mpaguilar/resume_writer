import logging
from pathlib import Path

import click
import docx
import rich
import tomli

from resume_writer.models.personal import Personal
from resume_writer.models.resume import Resume
from resume_writer.renderers.html_renderer import RenderResumeHtml
from resume_writer.renderers.markdown_renderer import RenderResumeMarkdown
from resume_writer.resume_render.ats.resume_main import (
    RenderResume as AtsRenderResume,
)
from resume_writer.resume_render.basic.resume_main import (
    RenderResume as BasicRenderResume,
)
from resume_writer.resume_render.plain.resume_main import (
    RenderResume as PlainRenderResume,
)
from resume_writer.resume_render.render_settings import ResumeRenderSettings
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
    log.info("Render of basic resume complete")


def ats_render(
    docx_doc: docx.document.Document,
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the ats renderer."""

    assert isinstance(docx_doc, docx.document.Document)
    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering simple resume")
    _renderer = AtsRenderResume(document=docx_doc, resume=resume, settings=settings)
    _renderer.render()
    log.info("Render of simple resume complete")


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


def html_render(
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the html renderer."""

    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering HTML resume")

    _html_renderer = RenderResumeHtml(
        resume=resume,
        settings=settings,
    )
    _html_renderer.render()
    _html_renderer.save(Path("data/html_resume.html"))

    log.info("Render of HTML resume complete.")

def markdown_render(
    resume: Resume,
    settings: ResumeRenderSettings,
) -> None:
    """Render the resume using the markdown renderer."""

    assert isinstance(resume, Resume)
    assert isinstance(settings, ResumeRenderSettings)

    log.info("Rendering Markdown resume")

    _markdown_renderer = RenderResumeMarkdown(
        resume=resume,
        settings=settings,
    )
    _markdown_renderer.render()
    _markdown_renderer.save(Path("data/markdown_resume.md"))

    log.info("Render of Markdown resume complete.")

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-file", type=click.Path(), default="data/resume.docx")
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
)
@click.option(
    "--resume-type",
    type=click.Choice(["ats", "basic", "plain", "html", "markdown"]),
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

    if resume_type == "basic":
        _docx_doc = docx.Document()
        basic_render(_docx_doc, _resume, _render_settings)
        _docx_doc.save(output_file)
    elif resume_type == "plain":
        _docx_doc = docx.Document()
        plain_render(_docx_doc, _resume, _render_settings)
        _docx_doc.save(output_file)
    elif resume_type == "ats":
        _docx_doc = docx.Document()
        ats_render(_docx_doc, _resume, _render_settings)
        _docx_doc.save(output_file)
    elif resume_type == "html":
        html_render(_resume, _render_settings)
    elif resume_type == "markdown":
        markdown_render(resume=_resume, settings=_render_settings)
    else:
        raise ValueError(f"Unknown resume type: {resume_type}")

    log.info(f"Saved resume to {output_file}")

    rich.print(_resume)


if __name__ == "__main__":
    main()
