# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how much of the service interval has been consumed, as a percentage.

    Examples:
        wear_percent(14900, 15000) -> 99.33...
        wear_percent(15000, 15000) -> 100.0
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True only when a car has a valid last-service reading and is >= 80% worn."""
    if "last_service_km" not in car:
        # No reading on file — cannot determine wear; do not flag.
        return False
    km_since = car["odometer"] - car["last_service_km"]
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that needs a service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
