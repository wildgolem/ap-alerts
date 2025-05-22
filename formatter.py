from config import COST, CPP, MAX_STOPS, MAX_DURATION
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
    return flight["MileageCost"] * CPP + flight["TotalTaxes"] / 100


def flight_sort_key(flight):
    return (compute_cost(flight), parse_departure_date(flight), flight["TotalDuration"])


def filter_flights(data):
    if not data:
        return []

    flights = []
    
    for flight in data:
        for trip in flight["AvailabilityTrips"]:
            if (trip["RemainingSeats"] > 0 and
                trip["Stops"] <= MAX_STOPS and
                trip["TotalDuration"] <= MAX_DURATION * 60 and
                compute_cost(trip) <= COST):
                flights.append(trip)

    return sorted(flights, key=flight_sort_key)


def format_flight(flight):
    origin = flight["OriginAirport"]
    destination = flight["DestinationAirport"]
    duration = round(flight["TotalDuration"] / 60)
    stops = flight["Stops"]
    connections = ", ".join(flight.get("Connections", []))
    layovers = "Direct" if stops == 0 else connections
    seats = flight["RemainingSeats"]
    cost = round(compute_cost(flight), 2)

    def format_time(key):
        dt = parse_datetime(flight.get(key, ""))
        return dt.strftime("%Y-%m-%d [%H:%M]") if dt else "Unknown"

    return (
        f"{origin} ↔ {destination} | {duration}h <{layovers}>\n"
        f"{format_time('DepartsAt')} → {format_time('ArrivesAt')}\n"
        f"${cost} ({seats} seats left)"
    )
