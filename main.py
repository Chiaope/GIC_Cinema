import uuid

class Cinema:
    def __init__(self, title, rows, seats_per_row):
        self.title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seating = [["." for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}
    
    def display_seating(self):
        print("\nSeating Layout:")
        for i, row in enumerate(self.seating):
            print(f"Row {chr(65 + i)}: {' '.join(row)}")
    
    def book_tickets(self, num_tickets, start_seat=None):
        available_seats = sum(row.count(".") for row in self.seating)
        if num_tickets > available_seats:
            print("Not enough seats available. Try again.")
            return
        
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

def main():
    title, rows, seats_per_row = input("Enter movie title and seating map (Title Rows SeatsPerRow): ").split()
    cinema = Cinema(title, int(rows), int(seats_per_row))
    
    while True:
        print(f"\nWelcome to GIC Cinemas")
        print("[1] Book tickets")
        print("[2] Check bookings")
        print("[3] Exit")
        choice = input("Enter your selection: ")
        
        if choice == "1":
            num_tickets = int(input("Enter number of tickets: "))
            start_seat = input("Enter preferred seat (e.g., B03) or press Enter for default: ").strip()
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

if __name__ == "__main__":
    main()
