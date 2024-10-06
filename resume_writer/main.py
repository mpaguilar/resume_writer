import logging
from datetime import datetime
from pathlib import Path

import click
import docx
import rich
import tomli
from jinja2 import Environment, PackageLoader, select_autoescape
from resume_render.resume_render_text_base import HtmlDoc

from resume_writer.models.personal import Personal
from resume_writer.models.resume import Resume
from resume_writer.resume_render.ats.resume_main import (
    RenderResume as AtsRenderResume,
)
from resume_writer.resume_render.basic.resume_main import (
    RenderResume as BasicRenderResume,
)
from resume_writer.resume_render.html.resume_main import (
    RenderResume as HtmlRenderResume,
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

    def date_filter(resdate: datetime | None, date_format: str = "%B %Y") -> str:
        """Format dates in jinja template. Returns 'present' if passed None."""
        assert isinstance(resdate, (datetime, type(None))), "Invalid datetime"
        assert isinstance(date_format, str), "Invalid date format"

        if resdate is None:
            return "Present"

        return resdate.strftime(date_format)

    def lf_to_br(text: str) -> str:
        """Convert line feeds to html breaks."""
        assert isinstance(text, str)
        _txt = text.replace("\r\n", "\n")
        _txt = _txt.replace("\n\n", "\n")
        _txt = _txt.replace("\n", "<br>")
        return _txt

    def list_len(lst: list) -> int:
        """Return the length of a list."""
        assert isinstance(lst, list)
        return len(lst)

    jinja_env = Environment(
        loader=PackageLoader("resume_render.html"),
        autoescape=select_autoescape(),
    )
    jinja_env.filters["date"] = date_filter
    jinja_env.filters["lf_to_br"] = lf_to_br
    jinja_env.filters["list_len"] = list_len

    _document: HtmlDoc = HtmlDoc()
    _renderer = HtmlRenderResume(
        document=_document,
        jinja_env=jinja_env,
        resume=resume,
        settings=settings,
    )

    _renderer.render()
    _renderer.save(Path("data/html_resume.html"))

    log.info("Render of HTML resume complete.")


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-file", type=click.Path(), default="data/resume.docx")
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
)
@click.option(
    "--resume-type",
    type=click.Choice(["ats", "basic", "plain", "html"]),
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
    else:
        raise ValueError(f"Unknown resume type: {resume_type}")

    log.info(f"Saved resume to {output_file}")

    rich.print(_resume)


if __name__ == "__main__":
    main()
