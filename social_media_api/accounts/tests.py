from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from rest_framework.authtoken.models import Token


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')

        self.user_data = {
            "username": "johnny",
            "email": "johnny@example.com",
            "password": "pass1234"
        }

    def test_user_registration(self):
        """Ensure a new user can register"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(User.objects.filter(username="johnny").exists())

    def test_user_login(self):
        """Ensure a user can log in and receive a token"""
        # First register user
        self.client.post(self.register_url, self.user_data)

        # Attempt login
        response = self.client.post(self.login_url, {
            "username": "johnny",
            "password": "pass1234"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_profile_access_requires_authentication(self):
        """Ensure profile cannot be accessed without a token"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_access_with_token(self):
        """Ensure authenticated user can access their profile"""
        # Register user
        reg = self.client.post(self.register_url, self.user_data)
        token = reg.data["token"]

        # Include token in header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "johnny")
