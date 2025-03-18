from pydantic import validate_call
from src.cinema import Cinema
from src.custom_exception import BreakOutOfLoop
from src.request_user_input import initalise_movie_request


@validate_call(config=dict(arbitrary_types_allowed=True))
def options_selection_request(cinema: Cinema):
    """
    Main menu for user to select different options in the movie booking system

    Args:
        cinema (Cinema): Cinema that the user wants to make booking
    """
    while True:
        try:
            print("Welcome to GIC Cinemas")
            print(
                f"[1] Book tickets for {cinema.title} ({cinema.get_available_seat_count()} seats available)")
            print("[2] Check bookings")
            print("[3] Exit")
            choice = input("Please enter your selection:\n")

            if choice == "1":
                cinema.option_1_process()
            elif choice == "2":
                cinema.option_2_process()
            elif choice == "3":
                cinema.option_3_process()
            else:
                print("Invalid option. Try again.")
        except BreakOutOfLoop:
            return


def start(updated: bool = False):
    """
    Start the GIC cinema booking system

    Args:
        updated (bool, optional): Use updated manual selected seating arangement logic. Defaults to False.
    """
    title, rows, seats_per_row = initalise_movie_request()
    cinema = Cinema(title, rows, seats_per_row, updated)
    options_selection_request(cinema)
