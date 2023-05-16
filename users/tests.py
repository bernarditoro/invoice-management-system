from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import User


# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        self.client_user = get_user_model().objects.create_client(
            email="client@email.com",
            username="testclient",
            first_name="Test",
            last_name="Client"
        )

    def test_model_setup(self):
        self.assertIsInstance(self.client_user, User)
        self.assertTrue(self.client_user.is_client)
