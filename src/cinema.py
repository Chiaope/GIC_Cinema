from copy import deepcopy
from pydantic import validate_call


from src.custom_exception import BreakOutOfLoop
from src.request_user_input import booking_id_request, number_of_ticket_request, select_seat_request


class Cinema:
    @validate_call
    def __init__(self, title: str, rows: int, seats_per_row: int) -> None:
        """
        Initate Cinema with title, rows and seats per row

        Args:
            title (str): Title of the movie
            rows (int): Number of rows in the cinema
            seats_per_row (int): Number of seats per row in the cinema
        """
        self.booking_id_prep = 'GIC'
        self.booking_id_buffer = '0000'
        self.title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seating = [["." for _ in range(seats_per_row)]
                        for _ in range(rows)]
        self.bookings = {}

    def get_available_seat_count(self) -> int:
        """
        Get the number of seats available

        Returns:
            int: Number of seats available
        """
        return sum(row.count(".") for row in self.seating)

    def option_1_process(self) -> None:
        """
        Run the process when '1' is selected.
        When user wants to make a booking
        """
        seats_available = self.get_available_seat_count()
        num_tickets = number_of_ticket_request(seats_available)
        if not num_tickets:
            return
        print(f'Successfully reserved {num_tickets} {self.title} tickets.')
        self.reserve_seats(num_tickets)
        return

    def option_2_process(self) -> None:
        """
        Run the process when '2' is selected.
        When users want to check their booking arrangement, this will ask for the booking id and then display the seating arrangement
        """
        while True:
            user_booking_id = booking_id_request(self.bookings)
            if not user_booking_id:
                return
            seating = self.generate_booking_id_seat_mapping(user_booking_id)
            self.display_seating(seating)

    def option_3_process(self) -> None:
        """
        Run the process when '3' is selected.
        """
        print("Thank you for using GIC Cinemas Booking System!")
        raise BreakOutOfLoop()

    def generate_booking_id(self) -> str:
        """
        Generates a booking id

        Returns:
            str: Returns the booking id
        """
        booking_id = str(len(self.bookings) + 1)
        booking_id = self.booking_id_prep + \
            self.booking_id_buffer[:-len(booking_id)] + booking_id
        return booking_id

    @validate_call
    def reserve_seats(self, num_tickets: int) -> None:
        """
        Reserve seats when user is trying to book the seats

        Args:
            num_tickets (int): Number of seats that the user is trying to book
        """
        booking_id = self.generate_booking_id()
        selected_seats, reserved_seat_mapping = self.default_generate_reserve_seat_mapping(
            num_tickets)
        while True:
            print(f'Booking id: {booking_id}')
            print('Selected seats:')
            self.display_seating(reserved_seat_mapping)
            user_select_seat_input = select_seat_request(
                self.rows, self.seats_per_row)
            if not user_select_seat_input:
                self.bookings[booking_id] = selected_seats
                for row, col in selected_seats:
                    self.seating[row][col] = '#'
                return
            selected_row = user_select_seat_input[0]
            selected_col = user_select_seat_input[1]
            selected_seats, reserved_seat_mapping = self.selected_seat_generate_reserve_seat_mapping(
                num_tickets, selected_row, selected_col)

    @validate_call
    def selected_seat_generate_reserve_seat_mapping(self, num_tickets: int, selected_row: int, selected_col: int) -> tuple:
        """
        Generate a seat mapping when the user select the seat position manually

        Args:
            num_tickets (int): Number of seats the user wants to book
            selected_row (int): The row index that the user had selected
            selected_col (int): The column index that the user had selected

        Returns:
            tuple (selected_seats, seating): Returns the selected seats and the seat reserved seat mapping
        """
        selected_seats = []
        row = selected_row
        col = selected_col
        cols = self.seats_per_row
        # Since nothing is confirmed yet so we make a copy instead of actually updating it
        seating = deepcopy(self.seating)
        # Try to fill up entire row 1st
        while num_tickets > 0 and col < self.seats_per_row:
            if seating[row][col] == '.':
                num_tickets -= 1
                seating[row][col] = 'o'
                selected_seats.append((row, col))
            col += 1

        # Fill up the remaining seats
        while num_tickets > 0:
            row -= 1
            if row < 0:  # Resets to the furthest row if there are not enough space in front anymore
                row = self.rows - 1
            mid = cols // 2
            left, right = mid, mid
            while num_tickets > 0 and (left >= 0 or right < cols):
                if left >= 0 and seating[row][left] == '.':
                    seating[row][left] = 'o'
                    selected_seats.append((row, left))
                    num_tickets -= 1

                if num_tickets > 0 and right < cols and seating[row][right] == '.':
                    seating[row][right] = 'o'
                    selected_seats.append((row, right))
                    num_tickets -= 1

                left -= 1
                right += 1

        return selected_seats, seating

    @validate_call
    def default_generate_reserve_seat_mapping(self, num_tickets: int) -> tuple:
        """
        Generate the default seating arrangement when the user wants to book seats

        Args:
            num_tickets (int): Number of seats the user wants to book

        Returns:
            tuple (selected_seats, seating): Returns the selected seats and the seat reserved seat mapping
        """
        selected_seats = []

        row = self.rows - 1
        cols = self.seats_per_row
        seating = deepcopy(self.seating)

        while num_tickets > 0 and row >= 0:
            mid = cols // 2
            left, right = mid, mid

            while num_tickets > 0 and (left >= 0 or right < cols):
                if left >= 0 and seating[row][left] == '.':
                    seating[row][left] = 'o'
                    selected_seats.append((row, left))
                    num_tickets -= 1

                if num_tickets > 0 and right < cols and seating[row][right] == '.':
                    seating[row][right] = 'o'
                    selected_seats.append((row, right))
                    num_tickets -= 1

                left -= 1
                right += 1

            row -= 1
        return selected_seats, seating

    @validate_call
    def generate_booking_id_seat_mapping(self, booking_id: str) -> list[list]:
        """
        Generate the seating arrangement when a booking id is provided

        Args:
            booking_id (str): Booking id for the seating arrangement the user wants to check

        Returns:
            list[list]: Returns the seating arrangement mapping
        """
        booked_seats = self.bookings[booking_id]
        seating = deepcopy(self.seating)
        for booked_row, booked_col in booked_seats:
            seating[booked_row][booked_col] = 'o'
        return seating

    @validate_call
    def display_seating(self, seating: list[list]) -> None:
        """
        Print out the seating arrangement for the provided seat mapping

        Args:
            seating (list[list]): Seat mapping that should be printed out
        """
        total_n_length = (self.seats_per_row + 1) * 2
        screen_str = "SCREEN"
        padding = (total_n_length - len(screen_str)) // 2
        print(f"{' ' * padding}{screen_str}{' ' * padding}")
        print("-" * total_n_length)
        for i, row in enumerate(seating):
            print(f"{chr(65 + i)} {' '.join(row)}")
        row_list = [' ']
        for n in range(self.seats_per_row):
            row_list.append(str(n+1))
        print(' '.join(row_list))
