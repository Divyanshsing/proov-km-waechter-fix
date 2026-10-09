# fleet_utils.py
# Helpers for fleet calculations.

MILES_PER_KM: float = 0.621371   # 1 km = 0.621371 miles (was 1.609, which is km-per-mile — inverted)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list of numbers, or 0.0 for an empty list."""
    if not values:
        return 0.0
    return sum(values) / len(values)
