import unittest
from unittest.mock import MagicMock, patch

from holiday_planner.holidayplanner_admin import *

from holiday_planner.pg_models import Country

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

class HolidayPlannerAdminTest(TestCase):

    @patch('holiday_planner.pg_models.Country.objects.get')
    def test_toggle_is_public(self, mock_get):
        # Set up a mock Country instance with is_public = False
        mock_country = MagicMock()
        mock_country.is_public = False

        # Configure the mock get method to return the mock Country instance
        mock_get.return_value = mock_country

        # Call the toggle_is_public method with a dummy iso code
        old_value, new_value = HolidayPlannerAdmin.toggle_is_public('US')

        # Check that the old and new values are correct
        self.assertEqual(old_value, False)
        self.assertEqual(new_value, True)    

    @patch('holiday_planner.pg_models.Country.objects.get')  
    def test_toggle_is_public_not_found(self, mock_get):
        # Configure the mock get method to raise a DoesNotExist exception
        mock_get.side_effect = Country.DoesNotExist

        # Call the toggle_is_public method with a dummy iso code and check for the exception
        with self.assertRaises(ObjectDoesNotExist):
            HolidayPlannerAdmin.toggle_is_public('ZZ')

if __name__ == '__main__':
    unittest.main()
