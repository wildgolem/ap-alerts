import requests
import os
import json


API_URL = "https://seats.aero/partnerapi/search"
HEADERS = {
    "accept": "application/json",
    "Partner-Authorization": os.environ["API_KEY"]
}


def build_url(origin, destination):
    return (
        f"{API_URL}?origin_airport={origin}"
        f"&destination_airport={destination}"
        f"&take=1000&order_by=lowest_mileage"
        f"&include_trips=true&only_direct_flights=true"
        f"&include_filtered=false&programs=aeroplan"
    )


def fetch_flights(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Failed to fetch data: {e}")
        return None
