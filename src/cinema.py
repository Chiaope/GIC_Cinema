from copy import deepcopy
import uuid

from pydantic import validate_call

from src.custom_exception import BreakOutOfLoop
from src.request_user_input import number_of_ticket_request, select_seat_request


class Cinema:
    @validate_call
    def __init__(self, title: str, rows: int, seats_per_row: int):
        """
        Initialise Cinema Instance
        """
        self.booking_id_prep = 'GIC'
        self.booking_id_buffer = '0000'
        self.title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seating = [["." for _ in range(seats_per_row)]
                        for _ in range(rows)]
        self.bookings = {}

    def get_available_seat_count(self):
        return sum(row.count(".") for row in self.seating)

    def optional_1_process(self):
        seats_available = self.get_available_seat_count()
        num_tickets = number_of_ticket_request(seats_available)
        if not num_tickets:
            return
        print(f'Successfully reserved {num_tickets} {self.title} tickets.')
        self.reserve_seats(num_tickets)
        return

    def optional_2_process(self):
        print('Ran option 2')
        return

    def optional_3_process(self):
        print('Ran option 3')
        print("Thank you for using GIC Cinemas Booking System!")
        raise BreakOutOfLoop()

    def generate_booking_id(self):
        booking_id = str(len(self.bookings) + 1)
        booking_id = self.booking_id_prep + \
            self.booking_id_buffer[:-len(booking_id)] + booking_id
        return booking_id

    def reserve_seats(self, num_tickets):
        booking_id = self.generate_booking_id()
        selected_seats, reserved_seat_mapping = self.default_generate_reserve_seat_mapping(num_tickets)
        while True:
            print(f'Booking id: {booking_id}')
            print('Selected seats:')
            self.display_seating(reserved_seat_mapping)
            user_select_seat_input = select_seat_request(self.rows, self.seats_per_row)
            if not user_select_seat_input:
                self.bookings[booking_id] = selected_seats
                for row, col in selected_seats:
                    self.seating[row][col] = '#'
                return
            selected_row = user_select_seat_input[0]
            selected_col = user_select_seat_input[1]
            selected_seats, reserved_seat_mapping = self.selected_seat_generate_reserve_seat_mapping(num_tickets, selected_row, selected_col)
    
    def selected_seat_generate_reserve_seat_mapping(self, num_tickets, selected_row, selected_col):
        selected_seats = []
        row = selected_row
        col = selected_col
        cols = self.seats_per_row
        seating = deepcopy(self.seating) # Since nothing is confirmed yet so we make a copy instead of actually updating it
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
            if row < 0: # Resets to the furthest row if there are not enough space in front anymore
                row = self.rows -1
            mid = cols// 2
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

    def default_generate_reserve_seat_mapping(self, num_tickets):
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

    def display_seating(self, seating):
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

    def book_tickets(self, num_tickets, start_seat=None):
        booked_seats = []

        if start_seat:
            row_index = ord(start_seat[0]) - 65
            seat_index = int(start_seat[1:]) - 1
            available = [j for j in range(
                seat_index, self.seats_per_row) if self.seating[row_index][j] == "O"]
            while num_tickets > 0 and available:
                seat = available.pop(0)
                self.seating[row_index][seat] = "X"
                booked_seats.append(f"{chr(65 + row_index)}{seat+1}")
                num_tickets -= 1

        for i in range(self.rows - 1, -1, -1):  # Start from last row
            middle = self.seats_per_row // 2
            available = [j for j in range(
                self.seats_per_row) if self.seating[i][j] == "O"]
            available.sort(key=lambda x: abs(x - middle))

            while num_tickets > 0 and available:
                seat = available.pop(0)
                self.seating[i][seat] = "X"
                booked_seats.append(f"{chr(65 + i)}{seat+1}")
                num_tickets -= 1

            if num_tickets == 0:
                break

        booking_id = str(uuid.uuid4())[:8]
        self.bookings[booking_id] = booked_seats
        print(f"Booking Confirmed! ID: {booking_id}")
        print("Seats Booked:", ", ".join(booked_seats))

    def check_bookings(self):
        if not self.bookings:
            print("No bookings found.")
        else:
            for bid, seats in self.bookings.items():
                print(f"Booking ID: {bid} - Seats: {', '.join(seats)}")


if __name__ == '__main__':
    abc = Cinema('movie', 5, 10)
    derp = abc.generate_reserve_seat_mapping(8)
    abc.display_seating()
