import requests
import os
import time
from formatter import format_flight


MAX_FIELDS = 25
WEBHOOK_DEPART = os.getenv("WEBHOOK_DEPART")
WEBHOOK_RETURN = os.getenv("WEBHOOK_RETURN")


def send_flight_batches(flights, webhook_url, emoji):
    total = len(flights)
    total_pages = (total + MAX_FIELDS - 1) // MAX_FIELDS

    for i in range(0, total, MAX_FIELDS):
        page_number = i // MAX_FIELDS + 1
        chunk = flights[i:i + MAX_FIELDS]
        embed = {
            "title": f"**{emoji} {total} flights found ({page_number} of {total_pages})**",
            "color": 5793266,
            "fields": [format_flight(f) for f in chunk]
        }
        payload = {"embeds": [embed]}

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Discord message (page {page_number}): {e}")
            if response is not None:
                print(f"Response text: {response.text}")

        time.sleep(1)


def send_discord_message(departing_flights, returning_flights):
    if departing_flights:
        send_flight_batches(departing_flights, WEBHOOK_DEPART, "🛫")

    if returning_flights:
        send_flight_batches(returning_flights, WEBHOOK_RETURN, "🛬")
