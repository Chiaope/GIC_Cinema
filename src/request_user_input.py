from pydantic import validate_call
from src.custom_exception import NotEnoughSeatsException
from src.util.convert_alphabet_index import convert_alphabet_index


def initalise_movie_request() -> tuple:
    """
    Ask user for inputs in order to initialise the cinema


    Raises:
        ValueError: When number of rows provided is more than the number of alphabets or when the input is invalid

    Returns:
        tuple (title, rows, seats_per_row): Returns the movie title, number of rows in the cinema, number of seats per row in the cinema
    """
    while True:
        try:
            initialisation_config = input(
                "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n")
            title, rows, seats_per_row = initialisation_config.split()
            rows = int(rows)
            seats_per_row = int(seats_per_row)
            if rows > 26 or rows <= 0 or seats_per_row <= 0:
                raise ValueError
            return title, rows, seats_per_row
        except ValueError:
            print('Invalid input, please try again.')


@validate_call
def number_of_ticket_request(available_count: int) -> int:
    """
    Ask user for the number of tickets needed

    Args:
        available_count (int): The number of seats remaining

    Raises:
        NotEnoughSeatsException: When the requested number of tickets is more than the number of seats available
        ValueError: When the input is invalid

    Returns:
        int: Number of tickets requested by the user
    """
    while True:
        try:
            num_tickets = input(
                "Enter number of tickets to book, or enter blank to go back to main menu:\n")
            if num_tickets == '':
                return
            num_tickets = int(num_tickets)
            if num_tickets > available_count:
                raise NotEnoughSeatsException(available_count)
            if num_tickets < 1:
                raise ValueError
            return num_tickets
        except ValueError:
            print('Invalid input, please try again.')
        except NotEnoughSeatsException as e:
            print(e)


@validate_call
def select_seat_request(row_count: int, col_count: int) -> tuple:
    """
    Ask user for the prefered seat position

    Args:
        row_count (int): Number of rows in the cinema
        col_count (int): Number of seats per row in the cinema

    Raises:
        ValueError: When the input seating position is not valid

    Returns:
        tuple (row_selected, col_selected): Returns the position of the seat position selected in their index form
    """
    while True:
        try:
            selected_seat = input(
                "Enter blank to accept seat selection, or enter new seating position\n")
            if selected_seat == '':
                return
            row_selected = selected_seat[0].upper()
            col_selected = int(selected_seat[1:])-1
            if not row_selected.isalpha():
                raise ValueError
            row_selected = convert_alphabet_index(row_selected)
            if row_selected < 0 or row_selected >= row_count or col_selected < 0 or col_selected >= col_count:
                raise ValueError
            return (row_selected, col_selected)
        except ValueError:
            print('Invalid input, please try again.')


@validate_call
def booking_id_request(bookings: dict) -> str:
    """
    Ask user for the booking id

    Args:
        bookings (dict): All the available bookings

    Raises:
        ValueError: When the booking id provided is invalid

    Returns:
        str: Returns the booking id that the user have provided
    """
    while True:
        try:
            booking_id = input(
                "Enter booking id, or enter blank to go back to main menu:\n").upper()
            if booking_id == '':
                return
            if booking_id not in bookings.keys():
                raise ValueError
            return booking_id
        except ValueError:
            print('Invalid input, please try again.')
