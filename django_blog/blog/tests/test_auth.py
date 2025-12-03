import io
from PIL import Image
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.middleware.csrf import get_token


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPass123!",
            email="test@example.com"
        )

    # -----------------------------------------------------
    # Registration Tests
    # -----------------------------------------------------
    def test_registration_success(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'NewStrongPass123!',
            'password2': 'NewStrongPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'Pass123!',
            'password2': 'Wrong123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_password_is_hashed(self):
        user = User.objects.get(username='testuser')
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))

    # -----------------------------------------------------
    # Login Tests
    # -----------------------------------------------------
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'WrongPass!'
        })
        self.assertEqual(response.status_code, 200)

    # -----------------------------------------------------
    # Logout Tests
    # -----------------------------------------------------
    def test_logout(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    # -----------------------------------------------------
    # Profile Access Tests
    # -----------------------------------------------------
    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # redirected to login

    def test_profile_loads_for_authenticated_user(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    # -----------------------------------------------------
    # Profile Update Tests
    # -----------------------------------------------------
    def test_profile_update(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.post(self.profile_url, {
            'email': 'updated@example.com',
            'bio': 'Updated bio content'
        })
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')

    # -----------------------------------------------------
    # Profile Picture Upload Test
    # -----------------------------------------------------
    def generate_test_image(self):
        """Generate an in-memory image for upload."""
        image = Image.new('RGB', (100, 100))
        file = io.BytesIO()
        image.save(file, 'png')
        file.seek(0)
        return file

    def test_profile_picture_upload(self):
        self.client.login(username='testuser', password='StrongPass123!')

        image_file = SimpleUploadedFile(
            "test.png",
            self.generate_test_image().read(),
            content_type="image/png"
        )

        response = self.client.post(self.profile_url, {
            'email': 'pic@example.com',
            'bio': 'With picture',
            'profile_picture': image_file
        })

        self.assertEqual(response.status_code, 302)

        # If you have a Profile model, this test should be adjusted accordingly
        self.user.refresh_from_db()

    # -----------------------------------------------------
    # CSRF Protection Tests
    # -----------------------------------------------------
    def test_csrf_token_present_on_forms(self):
        """CSRF token must be present in GET forms."""
        response = self.client.get(self.register_url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_csrf_protection_blocks_requests(self):
        """POST without CSRF token should fail."""
        client = Client(enforce_csrf_checks=True)

        response = client.post(self.register_url, {
            'username': 'csrfuser',
            'email': 'csrf@example.com',
            'password1': 'NewStrongPass123!',
            'password2': 'NewStrongPass123!'
        })

        self.assertEqual(response.status_code, 403)
