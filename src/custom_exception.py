class BackToMainMenu(Exception):
    """
    Used as a break to reset to main menu
    """
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return ""

class NotEnoughSeatsException(Exception):
    """
    Exception for when there are not enough seats
    """
    def __init__(self, seats_available, message="Sorry, there are only {seats_available} seats available."):
        self.seats_available = seats_available
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return self.message.format(seats_available=self.seats_available)
