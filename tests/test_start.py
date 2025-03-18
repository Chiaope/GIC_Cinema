import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

from src import start
from src.cinema import Cinema
from src.custom_exception import BreakOutOfLoop


class MockCinema(Cinema):
    def __init__(self, title, rows, seats_per_row, updated=False):
        super().__init__(title, rows, seats_per_row, updated)

    def option_1_process(self):
        print('Ran Option 1 Process')

    def option_2_process(self):
        print('Ran Option 2 Process')

    def option_3_process(self):
        print('Ran Option 3 Process')


class TestOptionsSelectionRequest(unittest.TestCase):
    def setUp(self):
        """
        Initialise a mock cinema instance
        """
        self.cinema = MockCinema('abc', 10, 5)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_non_numeric_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['non_numeric_input', BreakOutOfLoop()]
        start.options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid option. Try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_invalid_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['999', BreakOutOfLoop()]
        start.options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid option. Try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_1_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['1', BreakOutOfLoop()]
        start.options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 1 Process", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_2_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', BreakOutOfLoop()]
        start.options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 2 Process", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_3_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['3', BreakOutOfLoop()]
        start.options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 3 Process", std_out)


class TestStart(unittest.TestCase):
    @patch("builtins.input")
    def test_start(self, mock_input):
        mock_input.side_effect = ['abc 10 10', BreakOutOfLoop()]
        self.assertIsNone(start.start())


if __name__ == '__main__':
    unittest.main()
