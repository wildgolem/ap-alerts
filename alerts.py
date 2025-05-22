import requests
import os
import time
from formatter import format_flight


WEBHOOK_URL = os.getenv("WEBHOOK_FLIGHT")
ID_FILE = "id.txt"


def write_flights_to_file(flights, emoji, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{emoji} {len(flights)} flights found\n\n")
        for flight in flights:
            f.write(format_flight(flight))
            f.write("\n" + "-" * 40 + "\n")


def read_message_id():
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            return f.read().strip()
    return None


def write_message_id(message_id):
    with open(ID_FILE, "w") as f:
        f.write(message_id)


def delete_discord_message(webhook_url, message_id):
    url = f"{webhook_url}/messages/{message_id}"
    try:
        response = requests.delete(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete message {message_id}: {e}")
        if response is not None:
            print(f"Response text: {response.text}")


def send_files_to_discord(filenames, webhook_url):
    files = [(f"file{i+1}", (os.path.basename(name), open(name, "rb"))) for i, name in enumerate(filenames)]
    try:
        response = requests.post(webhook_url, files=files, timeout=10)
        response.raise_for_status()
        return response.json().get("id")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send files to Discord: {e}")
        if response is not None:
            print(f"Response text: {response.text}")
    finally:
        for _, file_tuple in files:
            file_tuple[1].close()


def send_discord_message(departing_flights, returning_flights):
    filenames = []

    if departing_flights:
        filename = "departings.txt"
        write_flights_to_file(departing_flights, "🛫", filename)
        filenames.append(filename)

    if returning_flights:
        filename = "returnings.txt"
        write_flights_to_file(returning_flights, "🛬", filename)
        filenames.append(filename)

    old_message_id = read_message_id()
    if old_message_id:
        delete_discord_message(WEBHOOK_URL, old_message_id)
        time.sleep(1)

    new_message_id = send_files_to_discord(filenames, WEBHOOK_URL)
    if new_message_id:
        write_message_id(new_message_id)
