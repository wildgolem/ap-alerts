import requests
import os
import json


API_URL = "https://seats.aero"
HEADERS = {
    "accept": "application/json",
    "Partner-Authorization": os.environ["API_KEY"]
}


def build_url(origin, destination):
    return (
        f"{API_URL}/partnerapi/search?origin_airport={origin}"
        f"&destination_airport={destination}"
        f"&take=1000&order_by=lowest_mileage"
        f"&include_trips=true&only_direct_flights=false"
        f"&include_filtered=false&programs=aeroplan"
    )


def fetch_flights(origin, destination):
    flights = []
    url = build_url(origin, destination)

    while url:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                flights.extend(data["data"])

            if data.get("hasMore") and data.get("moreURL"):
                url = f"{API_URL}{data['moreURL']}"
            else:
                break
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Failed to fetch data: {e}")
            break

    return flights
