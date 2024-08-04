import logging

import rich
from models.personal import Personal
from models.resume import Resume

log = logging.basicConfig(level=logging.DEBUG)


def print_personal(personal: Personal) -> None:
    """Print the personal information."""
    rich.print(f"[bold]Name:[/bold] {personal.contact_info.name}")
    rich.print(f"[bold]Email:[/bold] {personal.contact_info.email}")
    rich.print(f"[bold]Phone:[/bold] {personal.contact_info.phone}")


def dump_resume(resume: Resume) -> None:
    """Dump the resume to the console."""

    _personal = resume.personal
    print_personal(_personal)


def go() -> None:
    """Start the app."""

    with open("../tests/test_resume.md") as f:
        _resume_text = f.read()

    _resume_lines = _resume_text.split("\n")
    _resume = Resume.parse(_resume_lines)

    # dump the resume to the console
    dump_resume(_resume)


if __name__ == "__main__":
    go()
