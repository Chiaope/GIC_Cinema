import unittest

from tests.test_cinema_class import TestCinema
from tests.test_start import TestMain

# Import all test cases

# Create a test suite
def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMain))
    suite.addTest(unittest.makeSuite(TestCinema))  # Add more test cases
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(create_test_suite())