class RequiredFilesTest(TestCase):
    REQUIRED_FILES = [
        'api/views.py',
        'api/serializers.py',
        'api/urls.py',
    ]

    def test_required_files_exist(self):
        for file_path in self.REQUIRED_FILES:
            full_path = os.path.join(settings.BASE_DIR, file_path)
            self.assertTrue(
                os.path.exists(full_path),
                f"Missing required file: {file_path}"
            )
