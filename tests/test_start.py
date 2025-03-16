import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

from src.start import options_selection_request
from src.custom_exception import BreakOutOfLoop


class TestOptionsSelectionRequest(unittest.TestCase):
    def setUp(self):
        """
        Initialise a mock cinema instance
        """
        self.cinema = MagicMock()
        self.cinema.title = 'Mock_Movie_Title'
        self.cinema.get_seats_available.return_value = 50
        self.cinema.optional_1_process = lambda: print('Ran Option 1 Process')
        self.cinema.optional_2_process = lambda: print('Ran Option 2 Process')
        self.cinema.optional_3_process = lambda: print('Ran Option 3 Process')

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_non_numeric_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['non_numeric_input', BreakOutOfLoop()]
        options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid option. Try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_invalid_number_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['999', BreakOutOfLoop()]
        options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Invalid option. Try again.", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_1_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['1', BreakOutOfLoop()]
        options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 1 Process", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_2_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['2', BreakOutOfLoop()]
        options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 2 Process", std_out)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_options_selection_request_number_3_input(self, mock_stdout, mock_input):
        mock_input.side_effect = ['3', BreakOutOfLoop()]
        options_selection_request(self.cinema)
        std_out = mock_stdout.getvalue().split('\n')
        self.assertIn("Ran Option 3 Process", std_out)


if __name__ == '__main__':
    unittest.main()
