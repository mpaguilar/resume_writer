import logging

import rich
from resume_markdown import MarkdownResumeParser
from resume_model import Personal, Resume

log = logging.basicConfig(level=logging.DEBUG)

def print_personal(personal : Personal) -> None:
    """Print the personal information."""
    rich.print(f"[bold]Name:[/bold] {personal.personal_info.name}")
    rich.print(f"[bold]Email:[/bold] {personal.personal_info.email}")
    rich.print(f"[bold]Phone:[/bold] {personal.personal_info.phone}")

    _personal_info = personal.personal_info
    rich.print(f"[bold]Website:[/bold] {personal.website}")
    rich.print(f"[bold]LinkedIn:[/bold] {personal.linkedin}")
    rich.print(f"[bold]GitHub:[/bold] {personal.github}")
    rich.print(f"[bold]Twitter:[/bold] {personal.twitter}")
    rich.print(f"[bold]Work Authorization:[/bold] {personal.work_authorization}")


def dump_resume(resume : Resume) -> None:
    """Dump the resume to the console."""

    _personal = resume.personal
    print_personal(_personal)


def go() -> None:
    """Start the app."""
    _parser = MarkdownResumeParser("data/test_resume.md")

    _resume = _parser.parse()
    dump_resume(_resume)
    rich.print(_resume.stats())

if __name__ == "__main__":
    go()
