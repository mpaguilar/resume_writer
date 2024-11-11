from datetime import datetime

def format_date(date: datetime | None) -> str:
    """Format date as MM/YYYY.
    
    Args:
        date: The datetime object to format
        
    Returns:
        Formatted date string as MM/YYYY or empty string if date is None
    """
    if date is None:
        return ""
    return date.strftime("%m/%Y")
