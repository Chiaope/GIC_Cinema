import string

class CinemaBookingSystem:
    def __init__(self):
        self.movie_title = None
        self.rows = 0
        self.seats_per_row = 0
        self.seating_map = []
        self.bookings = {}
        self.booking_counter = 1

    def initialize_seating_map(self):
        self.seating_map = [['.' for _ in range(self.seats_per_row)] for _ in range(self.rows)]

    def display_seating_map(self, booking_seats=None):
        if booking_seats is None:
            booking_seats = set()
        print("\nSeating Map:")
        print("S C R E E N")
        print("---")
        for i in range(self.rows - 1, -1, -1):
            row_label = string.ascii_uppercase[i]
            row_display = [f"{row_label}"]
            for j in range(self.seats_per_row):
                if (i, j) in booking_seats:
                    row_display.append('0')
                elif self.seating_map[i][j] == '#':
                    row_display.append('#')
                else:
                    row_display.append('.')
            print(' '.join(row_display))
        print(' '.join([str(i + 1) for i in range(self.seats_per_row)]))

    def book_tickets(self):
        if not self.movie_title:
            print("No movie defined. Please define the movie title and seating map first.")
            return

        print(f"\nBooking tickets for {self.movie_title}")
        while True:
            num_tickets = input("Enter number of tickets to book, or enter blank to go back to main menu: ")
            if num_tickets == '':
                return
            try:
                num_tickets = int(num_tickets)
                if num_tickets <= 0:
                    print("Please enter a positive number.")
                    continue
                if num_tickets > self.rows * self.seats_per_row:
                    print("Not enough seats available.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        booking_seats = self.select_seats(num_tickets)
        if not booking_seats:
            print("Could not allocate seats. Please try again.")
            return

        booking_id = f"GIC{self.booking_counter:04d}"
        self.booking_counter += 1
        self.bookings[booking_id] = booking_seats
        for seat in booking_seats:
            self.seating_map[seat[0]][seat[1]] = '#'
        print(f"\nSuccessfully reserved {num_tickets} {self.movie_title} tickets.")
        print(f"Booking id: {booking_id}")
        self.display_seating_map(booking_seats)

        while True:
            new_position = input("Enter blank to accept seat selection, or enter new seating position: ")
            if new_position == '':
                print(f"Booking id: {booking_id} confirmed.")
                break
            else:
                try:
                    row_label = new_position[0].upper()
                    seat_number = int(new_position[1:]) - 1
                    row_index = string.ascii_uppercase.index(row_label)
                    if row_index >= self.rows or seat_number >= self.seats_per_row:
                        print("Invalid seating position. Please try again.")
                        continue
                    new_booking_seats = self.select_seats(num_tickets, (row_index, seat_number))
                    if new_booking_seats:
                        for seat in booking_seats:
                            self.seating_map[seat[0]][seat[1]] = '.'
                        booking_seats = new_booking_seats
                        for seat in booking_seats:
                            self.seating_map[seat[0]][seat[1]] = '#'
                        print(f"Booking id: {booking_id}")
                        self.display_seating_map(booking_seats)
                except (ValueError, IndexError):
                    print("Invalid seating position format. Please try again.")

    def select_seats(self, num_tickets, start_position=None):
        booking_seats = set()
        remaining_tickets = num_tickets

        if start_position:
            row, seat = start_position
            for j in range(seat, self.seats_per_row):
                if self.seating_map[row][j] == '.':
                    booking_seats.add((row, j))
                    remaining_tickets -= 1
                    if remaining_tickets == 0:
                        return booking_seats
            row -= 1

        for row in range(self.rows - 1, -1, -1):
            middle = self.seats_per_row // 2
            for seat in range(middle, self.seats_per_row):
                if self.seating_map[row][seat] == '.':
                    booking_seats.add((row, seat))
                    remaining_tickets -= 1
                    if remaining_tickets == 0:
                        return booking_seats
            if remaining_tickets == 0:
                break

        return booking_seats

    def check_bookings(self):
        if not self.bookings:
            print("No bookings have been made yet.")
            return

        print("\nCurrent Bookings:")
        for booking_id, seats in self.bookings.items():
            print(f"Booking ID: {booking_id}, Seats: {seats}")

    def run(self):
        while True:
            print("\nWelcome to GIC Cinemas")
            if self.movie_title:
                available_seats = sum(row.count('.') for row in self.seating_map)
                print(f"[1] Book tickets for {self.movie_title} ({available_seats} seats available)")
            else:
                print("[1] Book tickets (No movie defined)")
            print("[2] Check bookings")
            print("[3] Exit")
            choice = input("Please enter your selection: ")

            if choice == '1':
                if not self.movie_title:
                    movie_input = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format: ")
                    try:
                        title, rows, seats_per_row = movie_input.split()
                        self.rows = int(rows)
                        self.seats_per_row = int(seats_per_row)
                        if self.rows > 26 or self.seats_per_row > 50:
                            print("Maximum number of rows is 26 and maximum number of seats per row is 50.")
                            continue
                        self.movie_title = title
                        self.initialize_seating_map()
                    except ValueError:
                        print("Invalid input format. Please try again.")
                        continue
                self.book_tickets()
            elif choice == '2':
                self.check_bookings()
            elif choice == '3':
                print("Thank you for using GIC Cinemas system. Bye!")
                break
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    cinema = CinemaBookingSystem()
    cinema.run()