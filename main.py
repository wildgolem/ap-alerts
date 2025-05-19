
import requests
import json
import os


START = "YUL"
END = "NRT,ICN"
MAX_LAYOVER = 1
DIRECT_COST = 1150
LAYOVER_COST = 1000
DIRECT_DURATION = 15
LAYOVER_DURATION = 20


API_URL = "https://seats.aero/partnerapi/search"
HEADERS = {
    "accept": "application/json",
    "Partner-Authorization": os.environ["API_KEY"]
}


def build_url(origin, destination):
    return (
        f"{API_URL}"
        f"?origin_airport={origin}"
        f"&destination_airport={destination}"
        f"&cabin=economy"
        f"&take=1000"
        f"&order_by=lowest_mileage"
        f"&include_trips=true"
        f"&only_direct_flights=false"
        f"&include_filtered=false"
        f"&programs=aeroplan"
    )


def fetch_flights(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def filter_flights(data):
    filtered = []
    for entry in data.get("data", []):
        for trip in entry.get("AvailabilityTrips", []):
            #if trip["RemainingSeats"] <= 0:
            #    continue
            cost = trip["MileageCost"] * 0.02 + trip["TotalTaxes"] / 100
            if trip["Stops"] == 0 and cost <= DIRECT_COST and trip["TotalDuration"] <= DIRECT_DURATION*60:
                filtered.append(trip)
            elif trip["Stops"] <= MAX_LAYOVER and cost <= LAYOVER_COST and trip["TotalDuration"] <= LAYOVER_DURATION*60:
                filtered.append(trip)
    return filtered


def save_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    dep_url = build_url(START, END)
    dep_data = fetch_flights(dep_url)
    dep_filtered = filter_flights(dep_data)
    save_to_file(dep_filtered, "departing.json")

    ret_url = build_url(END, START)
    ret_data = fetch_flights(ret_url)
    ret_filtered = filter_flights(ret_data)
    save_to_file(ret_filtered, "returning.json")


if __name__ == "__main__":
    main()
