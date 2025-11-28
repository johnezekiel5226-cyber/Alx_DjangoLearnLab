import os
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.db import connection


class ProjectSetupTests(TestCase):

    def test_required_files_exist(self):
        """Checks for the required project files."""
        required_files = [
            'api/views.py',
            'api/serializers.py',
            'api/urls.py',
            'api/models.py',
            'api/tests',  # tests directory must exist
        ]

        for file_path in required_files:
            full_path = os.path.join(settings.BASE_DIR, file_path)
            self.assertTrue(
                os.path.exists(full_path),
                f"Required file is missing: {file_path}"
            )

    def test_test_implementation_exists(self):
        """Checks that tests have been implemented."""
        tests_path = os.path.join(settings.BASE_DIR, 'api', 'tests')
        files = os.listdir(tests_path)

        self.assertTrue(
            any(f.startswith('test_') and f.endswith('.py') for f in files),
            "No test files found! Implement tests inside api/tests/"
        )

    def test_endpoints_return_correct_status_codes(self):
        """Checks that the API endpoints return expected status codes."""

        # Example URL names you should adjust to match your actual project
        list_url = reverse('book-list')     # Should return 200 OK
        create_url = reverse('book-list')   # POST should return 201 CREATED

        # GET request should return 200
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

        # POST request should return 201
        post_response = self.client.post(create_url, {
            "title": "Test Book",
            "author": "Tester"
        })
        self.assertEqual(post_response.status_code, 201)

    def test_uses_separate_test_database(self):
        """Checks that Django is using a test database."""
        db_name = connection.settings_dict['NAME']
        self.assertTrue(
            'test' in db_name.lower(),
            f"Database is NOT a test database! Currently using: {db_name}"
        )
