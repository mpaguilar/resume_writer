import logging

import rich
from resume_markdown import MarkdownResumeParser

log = logging.basicConfig(level=logging.DEBUG)


def go() -> None:
    """Start the app."""
    _parser = MarkdownResumeParser("data/resume.md")

    _resume = _parser.parse()
    rich.print(_resume)
    rich.print(_resume.stats())

if __name__ == "__main__":
    go()
