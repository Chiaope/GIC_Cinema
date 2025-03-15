from src.cinema import Cinema


def start():
    while True:
        initialisation_config = input(
            "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")
        try:
            title, rows, seats_per_row = initialisation_config.split()
            cinema = Cinema(title, int(rows), int(seats_per_row))
            break
        except:
            print("Invalid movie definition, please try again.")

    while True:
        print("Welcome to GIC Cinemas")
        print(f"[1] Book tickets for {cinema.title} ({cinema.get_available_seat_count()} seats available)")
        print("[2] Check bookings")
        print("[3] Exit")
        choice = input("Please enter your selection:\n")

        if choice == "1":
            num_tickets = int(input("Enter number of tickets: "))
            start_seat = input(
                "Enter preferred seat (e.g., B03) or press Enter for default: ").strip()
            start_seat = start_seat if start_seat else None
            cinema.book_tickets(num_tickets, start_seat)
            cinema.display_seating()
        elif choice == "2":
            cinema.check_bookings()
        elif choice == "3":
            print("Thank you for using GIC Cinemas Booking System!")
            break
        else:
            print("Invalid option. Try again.")
