from config import RATE
from datetime import datetime


def parse_datetime(raw):
    try:
        return datetime.fromisoformat(raw.rstrip("Z"))
    except Exception:
        return None


def parse_departure_date(flight):
    dt = parse_datetime(flight.get("DepartsAt", ""))
    return dt if dt else datetime.max


def compute_cost(flight):
    return flight["MileageCost"] * RATE + flight["TotalTaxes"] / 100


def flight_sort_key(flight):
    return (compute_cost(flight), parse_departure_date(flight))


def filter_flights(data, max_cost):
    if not data:
        return []

    flights = []
    for entry in data.get("data", []):
        for trip in entry.get("AvailabilityTrips", []):
            if trip.get("RemainingSeats", 0) > 0 and compute_cost(trip) <= max_cost:
                flights.append(trip)

    return sorted(flights, key=flight_sort_key)


def format_flight(flight):
    origin = flight["OriginAirport"]
    destination = flight["DestinationAirport"]
    seats = flight["RemainingSeats"]
    cost = round(compute_cost(flight), 2)

    def format_time(key):
        dt = parse_datetime(flight.get(key, ""))
        return dt.strftime("%Y-%m-%d (%H:%M)") if dt else "Unknown"

    return {
        "name": "-----------------------------------\n" + f"{origin} ↔ {destination}",
        "value": (
            f"**Departure:** {format_time('DepartsAt')}\n"
            f"**Arrival:** {format_time('ArrivesAt')}\n"
            f"**Seats:** {seats}\n"
            f"**Cost:** ${cost}"
        ),
        "inline": False
    }
