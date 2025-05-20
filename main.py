from config import START, END, COST
from api import build_url, fetch_flights
from formatter import filter_flights
from alerts import send_discord_message


def main():
    dep_url = build_url(START, END)
    dep_data = fetch_flights(dep_url)
    dep_filtered = filter_flights(dep_data, COST)

    ret_url = build_url(END, START)
    ret_data = fetch_flights(ret_url)
    ret_filtered = filter_flights(ret_data, COST)

    send_discord_message(dep_filtered, ret_filtered)


if __name__ == "__main__":
    main()
