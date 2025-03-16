from pydantic import validate_call

from src.custom_exception import NotEnoughSeatsException
from src.util.convert_alphabet_index import convert_alphabet_index


def initalise_movie_request():
    """Ask user for inputs in order to initialise the cinema
    Returns:
        tuple: (Movie title, Number of rows in the cinema, Number of seats in each row in the cinema)
    """
    while True:
        try:
            initialisation_config = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n")
            title, rows, seats_per_row = initialisation_config.split()
            rows = int(rows)
            seats_per_row = int(seats_per_row)
            if rows > 26:
                raise ValueError
            return title, rows, seats_per_row
        except ValueError:
            print('Invalid input, please try again.')


def number_of_ticket_request(available_count: int):
    while True:
        try:
            num_tickets = input("Enter number of tickets to book, or enter blank to go back to main menu:\n")
            if num_tickets == '':
                return
            num_tickets = int(num_tickets)
            if num_tickets > available_count:
                raise NotEnoughSeatsException(available_count)
            return num_tickets
        except ValueError:
            print('Invalid input, please try again.')
        except NotEnoughSeatsException as e:
            print(e)
        
def select_seat_request():
    while True:
        try:
            selected_seat = input("Enter blank to accept seat selection, or enter new seating position\n")
            if selected_seat == '':
                return
            row_selected = selected_seat[0].upper()
            col_selected = int(selected_seat[1:])
            if not row_selected.isalpha():
                raise ValueError
            return [convert_alphabet_index(row_selected), col_selected-1]
        except ValueError:
            print('Invalid input, please try again.')

@validate_call
def booking_id_request(bookings: dict):
    while True:
        try:
            booking_id = input("Enter booking id, or enter blank to go back to main menu:\n").upper()
            if booking_id == '':
                return
            if booking_id not in bookings.keys():
                raise ValueError
            return bookings[booking_id]
        except ValueError:
            print('Invalid input, please try again.')
