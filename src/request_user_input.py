from src.custom_exception import BackToMainMenu


def initalise_movie_request():
    """Ask user for inputs in order to initialise the cinema
    Returns:
        tuple: (Movie title, Number of rows in the cinema, Number of seats in each row in the cinema)
    """
    while True:
        try:
            initialisation_config = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")
            title, rows, seats_per_row = initialisation_config.split()
            return title, int(rows), int(seats_per_row)
        except:
            print('Invalid input, please try again.')


def options_selection_request(cinema):
    """Main menu for user to select different options in the movie booking system

    Args:
        cinema (Cinema): Cinema that the user wants to make booking
    """
    while True:
        try:
            print("Welcome to GIC Cinemas")
            print(
                f"[1] Book tickets for {cinema.title} ({cinema.get_seats_available()} seats available)")
            print("[2] Check bookings")
            print("[3] Exit")
            choice = input("Please enter your selection:\n")

            if choice == "1":
                cinema.optional_1_process()
                # num_tickets = int(input("Enter number of tickets: "))
                # start_seat = input(
                #     "Enter preferred seat (e.g., B03) or press Enter for default: ").strip()
                # start_seat = start_seat if start_seat else None
                # cinema.book_tickets(num_tickets, start_seat)
                # cinema.display_seating()
            elif choice == "2":
                cinema.check_bookings()
            elif choice == "3":
                print("Thank you for using GIC Cinemas Booking System!")
                break
            else:
                print("Invalid option. Try again.")
        except Exception as e:
            print(e)


def number_of_ticket_request():
    num_tickets = int(input(
        "Enter number of tickets to book, or enter blank to go back to main menu:"))
    if num_tickets is None:
        raise BackToMainMenu()
    return num_tickets
