from datetime import timedelta
import re


def parseDuration(duration: str):
    """
    Parse a duration string
    Args:
        duration: the duration string

    Returns: the duration in seconds

    """
    pattern = re.compile(r"(\d+)\s*(seconds?|minutes?|hours?|days?)")
    match = pattern.match(duration)
    if not match:
        raise ValueError(f"Invalid duration string: {duration}")

    value, unit = match.groups()
    value = int(value)
    unit = unit.lower()

    if unit.startswith("second"):
        duration = timedelta(seconds=value)
    elif unit.startswith("minute"):
        duration = timedelta(minutes=value)
    elif unit.startswith("hour"):
        duration = timedelta(hours=value)
    elif unit.startswith("day"):
        duration = timedelta(days=value)
    else:
        raise ValueError(f"Unknown time unit: {unit}")

    return duration.total_seconds()
