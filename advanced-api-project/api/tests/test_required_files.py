import os
from django.test import TestCase
from django.conf import settings

class RequiredFileTest(TestCase):
    def test_required_file_exists(self):
        """
        Ensure that the required file exists in the project.
        """
        required_file_path = os.path.join(settings.BASE_DIR, 'api', 'views.py')
        
        self.assertTrue(
            os.path.exists(required_file_path),
            f"Required file not found: {required_file_path}"
        )
