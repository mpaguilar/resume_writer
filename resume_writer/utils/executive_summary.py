import logging

from resume_writer.models.experience import (
    Experience,
)

log = logging.getLogger(__name__)


class ExecutiveSummary:
    """Collect and return job summaries for given categories."""

    def __init__(self, experience: Experience):
        """Initialize the ExecutiveSummary class."""
        assert isinstance(
            experience,
            Experience,
        ), f"experience must be of the Experience class, received {type(experience)}"

        self.experience = experience

    def summary(self, categories: list[str]) -> dict[str, dict]:
        """Create a dictionary of roles and their summaries."""
        # Create a dictionary to hold the roles and their summaries
        _summaries = {}

        # Loop through the provided categories
        for _category in categories:
            # Filter the roles that belong to the current category

            if not _category:
                continue

            _category_roles = [
                role
                for role in self.experience.roles
                if role.basics.job_category == _category
            ]

            # If there are no roles in the current category, skip to the next category
            if not _category_roles:
                log.warning(f"No roles found for category: {_category}")
                continue

            # Create a list to hold the summaries for the current category
            _category_summaries = []

            # Create a list of summaries for the current category
            for _role in _category_roles:
                if not _role.summary.summary:
                    log.warning(f"No summary for {_role.basics.title}")
                    continue

                _summary = {
                    "summary": _role.summary.summary,
                    "company": _role.basics.company,
                    "first_date": _role.basics.start_date,
                    "last_date": _role.basics.end_date,
                    "title": _role.basics.title,
                }
                _category_summaries.append(_summary)
            _summaries[_category] = _category_summaries

        return _summaries

    def available_categories(self) -> list[str]:
        """Return a list of role categories."""
        _categories = [_role.basics.job_category for _role in self.experience.roles]
        _categories = list(set(_categories))

        return _categories
