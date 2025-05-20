import requests
import os
import time
from formatter import format_flight


MAX_FIELDS = 25
WEBHOOK_DEPART = os.getenv("WEBHOOK_DEPART")
WEBHOOK_RETURN = os.getenv("WEBHOOK_RETURN")


def send_flight_batches(title, flights, emoji, webhook_url):
        for i in range(0, len(flights), MAX_FIELDS):
            chunk = flights[i:i + MAX_FIELDS]
            embed = {
                "title": f"{emoji} {title} (Page {i // MAX_FIELDS + 1})",
                "color": 5814783,
                "fields": [format_flight(f) for f in chunk]
            }
            payload = {"embeds": [embed]}

            try:
                response = requests.post(webhook_url, json=payload, timeout=10)
                response.raise_for_status()
                print(f"Sent page {i // MAX_FIELDS + 1} for {title}.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send Discord message (page {i // MAX_FIELDS + 1}): {e}")
                if response is not None:
                    print(f"Response text: {response.text}")

            time.sleep(1)


def send_discord_message(departing_flights, returning_flights):
    if departing_flights:
        send_flight_batches("Departing Flights", departing_flights, "🛫", WEBHOOK_DEPART)

    if returning_flights:
        send_flight_batches("Returning Flights", returning_flights, "🛬", WEBHOOK_RETURN)
