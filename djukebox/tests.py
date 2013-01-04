"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


# TO DO (random things, not comprehensive!):
#   - check that upon logging out/in/after registering, etc., end up at same place where initiated that action
#   - successful registration - get logged in automatically