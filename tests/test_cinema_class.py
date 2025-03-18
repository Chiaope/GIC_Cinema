from io import StringIO
import unittest
from unittest.mock import MagicMock, patch

from pydantic import ValidationError

from src import cinema
from src.custom_exception import BreakOutOfLoop, NotEnoughSeatsException


class TestCinema(unittest.TestCase):
    def setUp(self):
        self.title = "MockMovie"
        self.rows = 10
        self.seats_per_row = 10
        self.cinema = cinema.Cinema(self.title, self.rows, self.seats_per_row)

    def test_cinema_initiated_invalid_title_type(self):
        with self.assertRaises(ValidationError):
            cinema.Cinema(321, 10, 10)

    def test_cinema_initiated_invalid_row_type(self):
        with self.assertRaises(ValidationError):
            cinema.Cinema('Movie', 'ten', 10)

    def test_cinema_initiated_invalid_seats_per_row_type(self):
        with self.assertRaises(ValidationError):
            cinema.Cinema('Movie', 10, 'ten')

    def test_cinema_initiated_valid_input(self):
        # Pydantic automatically convert strings to int if it does not raise exception
        c = cinema.Cinema('Movie', '10', 10)
        self.assertIsInstance(c, cinema.Cinema)

    def test_get_available_seat_count_after_initialising(self):
        results = self.cinema.get_available_seat_count()
        self.assertEqual(self.rows*self.seats_per_row, results)

    @patch("builtins.input")
    def test_get_available_seat_count_after_booking(self, mock_input):
        mock_input.side_effect = ['']
        num_tickets = 33
        self.cinema.reserve_seats(num_tickets)
        results = self.cinema.get_available_seat_count()
        self.assertEqual((self.rows * self.seats_per_row) -
                         num_tickets, results)

    @patch("builtins.input")
    def test_option_1_process_go_main_menu(self, mock_input):
        mock_input.side_effect = ['']

        self.assertIsNone(self.cinema.option_1_process())

    @patch("builtins.input")
    def test_option_1_process_reserve_seats(self, mock_input):
        mock_input.side_effect = [3, '']

        self.assertIsNone(self.cinema.option_1_process())

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input")
    def test_option_1_process_not_enough_seats(self, mock_input, mock_stdout):
        mock_available_seats = MagicMock()
        mock_available_seats.return_value = 0
        c = cinema.Cinema('not_enough_seats_movie', 5, 5)
        c.get_available_seat_count = mock_available_seats
        c.option_1_process()
        std_out = mock_stdout.getvalue().split('\n')

        self.assertIn("There are no more seats.", std_out)

    @patch(f"{cinema.__name__}.Cinema.generate_booking_id")
    @patch("builtins.input")
    def test_option_2_process_check_booking(self, mock_input, mock_generate_booking_id):
        mock_booking_id = 'MOCK123'
        mock_generate_booking_id.return_value = mock_booking_id
        mock_input.side_effect = ['', mock_booking_id, '']
        self.cinema.reserve_seats(3)

        self.assertIsNone(self.cinema.option_2_process())

    def test_option_3_process_ran(self):
        with self.assertRaises(BreakOutOfLoop):
            self.cinema.option_3_process()

    def test_generate_booking_id_generated(self):
        current_number_of_bookings = len(self.cinema.bookings)
        new_number_of_bookings_str = str(current_number_of_bookings + 1)
        booking_id = self.cinema.booking_id_prep + \
            self.cinema.booking_id_buffer[:-len(
                new_number_of_bookings_str)] + new_number_of_bookings_str
        self.assertEqual(booking_id, self.cinema.generate_booking_id())

    @patch("builtins.input")
    def test_reserve_seats_accept_detault(self, mock_input):
        mock_input.side_effect = ['']
        num_tickets = 5
        self.assertIsNone(self.cinema.reserve_seats(num_tickets))

    @patch("builtins.input")
    def test_reserve_seats_user_select_seat_postion(self, mock_input):
        mock_input.side_effect = ['B3', '']
        num_tickets = 5
        self.assertIsNone(self.cinema.reserve_seats(num_tickets))

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_non_updated_reserve_seats_user_select_seat_postion_overflow(self, mock_stdout, mock_input):
        mock_input.side_effect = ['B3', BreakOutOfLoop()]
        num_tickets = 8
        c = cinema.Cinema('mock_updated_movie', 3, 3)

        with self.assertRaises(BreakOutOfLoop):
            c.reserve_seats(num_tickets)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn(
            'Sorry, there are only 4 seats available from the selected position.', std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_updated_reserve_seats_user_select_seat_postion_overflow(self, mock_stdout, mock_input):
        mock_input.side_effect = ['B3', BreakOutOfLoop()]
        num_tickets = 8
        c = cinema.Cinema('mock_updated_movie', 3, 3, updated=True)

        with self.assertRaises(BreakOutOfLoop):
            c.reserve_seats(num_tickets)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertNotIn(
            'Sorry, there are only 4 seats available from the selected position.', std_out)

    def test_selected_seat_generate_reserve_seat_mapping(self):
        num_tickets = 4
        selected_row = 1
        selected_col = 2
        select_seats_check = [(1, 2), (0, 1), (0, 0), (0, 2)]
        seat_mapping_check = [
            ['o', 'o', 'o'],
            ['.', '.', 'o'],
            ['.', '.', '.']
        ]
        c = cinema.Cinema('Small', 3, 3)

        results = c.selected_seat_generate_reserve_seat_mapping(
            num_tickets, selected_row, selected_col)
        self.assertEqual((select_seats_check, seat_mapping_check), results)

    def test_non_updated_selected_seat_generate_reserve_seat_mapping(self):
        num_tickets = 5
        selected_row = 1
        selected_col = 2

        c = cinema.Cinema('Small', 3, 3)
        with self.assertRaises(NotEnoughSeatsException):
            c.selected_seat_generate_reserve_seat_mapping(
                num_tickets, selected_row, selected_col)

    def test_updated_selected_seat_generate_reserve_seat_mapping(self):
        num_tickets = 5
        selected_row = 1
        selected_col = 2
        select_seats_check = [(1, 2), (0, 1), (0, 0), (0, 2), (2, 1)]

        seat_mapping_check = [
            ['o', 'o', 'o'],
            ['.', '.', 'o'],
            ['.', 'o', '.']
        ]

        c = cinema.Cinema('Small', 3, 3, updated=True)
        results = c.selected_seat_generate_reserve_seat_mapping(
            num_tickets, selected_row, selected_col)
        self.assertEqual((select_seats_check, seat_mapping_check), results)

    def test_default_generate_reserve_seat_mapping(self):
        num_tickets = 5
        select_seats_check = [(2, 1), (2, 0), (2, 2), (1, 1), (1, 0)]
        seat_mapping_check = [
            ['.', '.', '.'],
            ['o', 'o', '.'],
            ['o', 'o', 'o']
        ]
        c = cinema.Cinema('Small', 3, 3)

        results = c.default_generate_reserve_seat_mapping(num_tickets)
        self.assertEqual((select_seats_check, seat_mapping_check), results)

    @patch(f"{cinema.__name__}.Cinema.generate_booking_id")
    @patch("builtins.input")
    def test_generate_booking_id_seat_mapping(self, mock_input, mock_generate_booking_id):
        mock_input.side_effect = ['']
        mock_booking_id = 'MOCK123'
        mock_generate_booking_id.return_value = mock_booking_id
        num_tickets = 5
        c = cinema.Cinema('Small', 3, 3)
        c.reserve_seats(num_tickets)
        seat_mapping_check = [
            ['.', '.', '.'],
            ['o', 'o', '.'],
            ['o', 'o', 'o']
        ]
        results = c.generate_booking_id_seat_mapping(mock_booking_id)
        self.assertEqual(seat_mapping_check, results)

    def test_display_seating(self):
        c = cinema.Cinema('Small', 3, 3)
        mock_seat_mapping = [
            ['.', '.', '.'],
            ['o', 'o', '.'],
            ['o', 'o', 'o']
        ]
        self.assertIsNone(c.display_seating(mock_seat_mapping))


if __name__ == '__main__':
    unittest.main()
