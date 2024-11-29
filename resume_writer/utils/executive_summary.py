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

    def summary(self, categories: list[str]) -> dict:
        """Create a dictionary of roles and their summaries."""

        # Create a dictionary to hold the roles and their summaries
        summaries = {}

        # Loop through the provided categories
        for category in categories:
            # Filter the roles that belong to the current category
            category_roles = [
                role
                for role in self.experience.roles
                if role.basics.job_category == category
            ]

            # If there are no roles in the current category, skip to the next category
            if not category_roles:
                continue

            # Create a list to hold the summaries for the current category
            category_summaries = []

            # Create a list of summaries for the current category
            category_summaries = [
                role.summary.summary for role in category_roles if role.summary.summary
            ]

            # Add the list of summaries for the current category to the dictionary
            summaries[category] = category_summaries

        return summaries
