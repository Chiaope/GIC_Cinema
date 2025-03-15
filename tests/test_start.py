import unittest
from unittest.mock import patch
from io import StringIO

from src import start


class TestMain(unittest.TestCase):
    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_main(self, mock_stdout, mock_input):
    #     # Simulate user input
    #     mock_input.side_effect = [
    #         "Avengers 5 10",  # Initial input: title, rows, seats_per_row
    #         "1",               # Book tickets
    #         "2",               # Number of tickets
    #         "",                # Default seat
    #         "2",               # Check bookings
    #         "3",               # Exit
    #     ]

    #     # Call the main function
    #     start.start()

    #     # Capture the output
    #     output = mock_stdout.getvalue()

    #     # Assert expected output
    #     self.assertIn("Welcome to GIC Cinemas", output)
    #     self.assertIn("Bookings: A01, A02", output)
    #     self.assertIn(
    #         "Thank you for using GIC Cinemas Booking System!", output)

    @patch("builtins.input")
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_initalisation(self, mock_stdout, mock_input):
        mock_input.side_effect = ["not a movie and seats", "Valid 1 2", "3"]
        std_out = mock_stdout.getvalue()
        start.start()
        self.assertEqual('Invalid movie definition, please try again.', std_out.split('\n'))
        
    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_valid_initalisation(self, mock_stdout, mock_input):
    #     mock_input.side_effect = "1"
    #     std_out = mock_stdout.getvalue()
    #     self.assertEqual('', std_out)

    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_invalid_input_selected(self, mock_stdout, mock_input):
    #     mock_input.side_effect = "abc"
    #     std_out = mock_stdout.getvalue()
    #     self.assertEqual('', std_out)


    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_input_1_selected(self, mock_stdout, mock_input):
    #     mock_input.side_effect = "1"
    #     std_out = mock_stdout.getvalue()
    #     self.assertEqual('', std_out)

    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_input_2_selected(self, mock_stdout, mock_input):
    #     mock_input.side_effect = "2"
    #     std_out = mock_stdout.getvalue()
    #     self.assertEqual('', std_out)

    # @patch("builtins.input")
    # @patch("sys.stdout", new_callable=StringIO)
    # def test_input_3_selected(self, mock_stdout, mock_input):
    #     mock_input.side_effect = "3"    
    #     std_out = mock_stdout.getvalue()
    #     self.assertEqual('', std_out)

if __name__ == "__main__":
    unittest.main()
