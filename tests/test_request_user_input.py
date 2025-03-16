from io import StringIO
import unittest
from unittest.mock import patch

from src.custom_exception import BreakOutOfLoop
from src.request_user_input import booking_id_request, initalise_movie_request, number_of_ticket_request, select_seat_request


class TestInitialiseMovieRequest(unittest.TestCase):
    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_initalise_movie_request_too_little_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['invalid input', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            initalise_movie_request()
        std_out = mock_stdout.getvalue().split('\n')
        self.assertEqual('Invalid input, please try again.', std_out[0])

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_initalise_movie_request_too_many_input(self, mock_stdout, mock_input):
        mock_input.side_effect = [
            'multiple worded movie 5 10', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            initalise_movie_request()
        std_out = mock_stdout.getvalue().split('\n')
        self.assertEqual('Invalid input, please try again.', std_out[0])

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_initalise_movie_request_non_numeric_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['number_word five ten', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            initalise_movie_request()
        std_out = mock_stdout.getvalue().split('\n')
        self.assertEqual('Invalid input, please try again.', std_out[0])

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_initalise_movie_request_too_many_rows_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['too_many_rows 27 10', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            initalise_movie_request()
        std_out = mock_stdout.getvalue().split('\n')
        self.assertEqual('Invalid input, please try again.', std_out[0])

    @patch("builtins.input")
    def test_initalise_movie_request_valid_input(self, mock_input):
        mock_input.side_effect = ['movie_title 5 10']
        results = initalise_movie_request()
        self.assertEqual(('movie_title', 5, 10), results)


class TestNumberOfTicketRequest(unittest.TestCase):
    def setUp(self):
        self.seats_available = 10

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_non_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['non numeric input', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            number_of_ticket_request(self.seats_available)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_too_many_tickets_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['100', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            number_of_ticket_request(self.seats_available)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn(
            f"Sorry, there are only {self.seats_available} seats available.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_negative_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['-5', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            number_of_ticket_request(self.seats_available)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_float_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['10.123', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            number_of_ticket_request(self.seats_available)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    def test_number_of_ticket_request_blank_input(self, mock_input):
        mock_input.side_effect = ['']
        results = number_of_ticket_request(self.seats_available)
        self.assertEqual(None, results)

    @patch("builtins.input")
    def test_number_of_ticket_request_numeric_input(self, mock_input):
        mock_input.side_effect = ['5']
        results = number_of_ticket_request(self.seats_available)
        self.assertEqual(5, results)


class TestSpecificSeatRequest(unittest.TestCase):
    def setUp(self):
        self.row_count = 5
        self.col_count = 5

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_invalid_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['definitely not a seat', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            select_seat_request(self.row_count, self.col_count)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_too_many_seats_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['B3 B4 B5', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            select_seat_request(self.row_count, self.col_count)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_number_of_ticket_request_invalid_seats_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['ABC33', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            select_seat_request(self.row_count, self.col_count)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    def test_number_of_ticket_request_blank_input(self, mock_input):
        mock_input.side_effect = ['']
        results = select_seat_request(self.row_count, self.col_count)
        self.assertEqual(None, results)

    @patch("builtins.input")
    def test_number_of_ticket_request_valid_input(self, mock_input):
        mock_input.side_effect = ['B3']
        results = select_seat_request(self.row_count, self.col_count)
        self.assertEqual((1, 2), results)


class TestBookingIDRequest(unittest.TestCase):
    def setUp(self):
        self.bookings = {'GIC0001': ['B5,B6'], 'GIC0002': ['C5,C6']}

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_booking_id_request_invalid_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['not a booking id', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            booking_id_request(self.bookings)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_booking_id_request_incorrect_booking_id_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['GIC01', BreakOutOfLoop()]
        with self.assertRaises(BreakOutOfLoop):
            booking_id_request(self.bookings)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid input, please try again.", std_out)

    @patch("builtins.input")
    def test_booking_id_request_correct_booking_id_input(self, mock_input):
        mock_input.side_effect = ['GIC0001']
        results = booking_id_request(self.bookings)
        self.assertEqual('GIC0001', results)


if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestNumberOfTicketRequest)
    # unittest.TextTestRunner().run(suite)

    unittest.main()
