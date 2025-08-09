from datetime import datetime


def format_date(date: datetime | None) -> str:
    """Format date as MM/YYYY.

    Args:
        date (datetime | None): The datetime object to format. If None, returns an empty string.

    Returns:
        str: Formatted date string as MM/YYYY or empty string if date is None.

    Notes:
        1. Check if the date is None. If so, return an empty string.
        2. If date is not None, use the strftime method to format the date as MM/YYYY.
        3. The formatted string is returned.
    """
    if date is None:
        return ""
    return date.strftime("%m/%Y")
