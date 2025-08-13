import logging

from resume_writer.models.experience import (
    Experience,
)

log = logging.getLogger(__name__)


class ExecutiveSummary:
    """Collect and return job summaries for given categories.

    Attributes:
        experience (Experience): The experience data to summarize, must be an instance of the Experience class.

    Args:
        experience (Experience): The experience data to summarize.
    """

    def __init__(self, experience: Experience):
        """Initialize the ExecutiveSummary class.

        Args:
            experience (Experience): The experience data to summarize.

        Notes:
            1. Validates that the provided experience is an instance of the Experience class.
            2. If not, raises an AssertionError with a descriptive message.
            3. Stores the experience instance as an instance variable.
        """
        assert isinstance(
            experience,
            Experience,
        ), f"experience must be of the Experience class, received {type(experience)}"

        self.experience = experience

    def summary(self, categories: list[str]) -> dict[str, dict]:
        """Create a dictionary of roles and their summaries.

        Args:
            categories (list[str]): A list of job categories to generate summaries for.

        Returns:
            dict[str, dict]: A dictionary where keys are category names and values are lists of summary dictionaries.
            Each summary dictionary contains:
                - "summary" (str): The role summary text.
                - "company" (str): The company name.
                - "first_date" (str): The start date of the role.
                - "last_date" (str): The end date of the role.
                - "title" (str): The job title.

        Notes:
            1. Initializes an empty dictionary to hold summaries by category.
            2. Iterates over each provided category.
            3. Filters roles belonging to the current category from the experience data.
            4. Skips categories with no matching roles and logs a warning.
            5. For each role in the category:
                a. Checks if a summary exists; if not, logs a warning and skips.
                b. Constructs a summary dictionary with relevant role details.
                c. Appends the dictionary to a list for the category.
            6. Adds the list of summaries to the result dictionary under the category key.
            7. Returns the final dictionary.
        """
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
        """Return a list of role categories.

        Returns:
            list[str]: A list of unique job categories found in the experience data.

        Notes:
            1. Extracts the job category from each role in the experience data.
            2. Converts the list of categories to a set to remove duplicates.
            3. Converts the set back to a list.
            4. Returns the list of unique categories.
        """
        _categories = [_role.basics.job_category for _role in self.experience.roles]
        _categories = list(set(_categories))

        return _categories
