from config import START, END
from api import fetch_flights
from formatter import filter_flights
from alerts import send_discord_message


def main():
    dep_data = fetch_flights(START, END)
    dep_filtered = filter_flights(dep_data)

    ret_data = fetch_flights(END, START)
    ret_filtered = filter_flights(ret_data)

    send_discord_message(dep_filtered, ret_filtered)


if __name__ == "__main__":
    main()
