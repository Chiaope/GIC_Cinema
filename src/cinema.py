import uuid

from src.custom_exception import NotEnoughSeatsException
from src.request_user_input import initalise_movie_request, number_of_ticket_request

class Cinema:
    def __init__(self):
        """Initialise Cinema Instance
        """
        self.booking_id_prep = 'GIC'
        self.booking_id_buffer = '0000'
        self.seating = [["." for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}
        
        title, rows, seats_per_row  = initalise_movie_request()
        self.title = title
        self.rows = int(rows)
        self.seats_per_row = int(seats_per_row)
        
    def get_available_seat_count(self):
        return sum(row.count(".") for row in self.seating)
    
    def optional_1_process(self):
        num_tickets = number_of_ticket_request()
        seats_available = self.get_available_seat_count()
        if num_tickets > seats_available:
            raise NotEnoughSeatsException(seats_available)
        
        print(f'Successfully reserved {num_tickets} {self.title} tickets.')
        booking_id = self.generate_booking_id()
        print(f'Booking id: {booking_id}')
        start_seat = input(
                    "Enter preferred seat (e.g., B03) or press Enter for default: ").strip()
        start_seat = start_seat if start_seat else None
        self.book_tickets(num_tickets, start_seat)
        self.display_seating()
        return
    
    def generate_booking_id(self):
        booking_id = str(len(self.bookings) + 1)
        booking_id = self.booking_id_prep + self.booking_id_buffer[:-len(booking_id)] + booking_id
        return booking_id
    
    def reserve_seats(self):
        return
    
    def display_seating(self):
        print("\nSeating Layout:")
        for i, row in enumerate(self.seating):
            print(f"Row {chr(65 + i)}: {' '.join(row)}")
    
    def book_tickets(self, num_tickets, start_seat=None):
        booked_seats = []
        
        if start_seat:
            row_index = ord(start_seat[0]) - 65
            seat_index = int(start_seat[1:]) - 1
            available = [j for j in range(seat_index, self.seats_per_row) if self.seating[row_index][j] == "O"]
            while num_tickets > 0 and available:
                seat = available.pop(0)
                self.seating[row_index][seat] = "X"
                booked_seats.append(f"{chr(65 + row_index)}{seat+1}")
                num_tickets -= 1
        
        for i in range(self.rows - 1, -1, -1):  # Start from last row
            middle = self.seats_per_row // 2
            available = [j for j in range(self.seats_per_row) if self.seating[i][j] == "O"]
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
    def generate_booking_id():
        booking_id = str(len({'GIC0001': 'DERP'}) + 100000000000000)
        booking_id = 'GIC' + '0000'[:-len(booking_id)] + booking_id
        return booking_id
    print(generate_booking_id())