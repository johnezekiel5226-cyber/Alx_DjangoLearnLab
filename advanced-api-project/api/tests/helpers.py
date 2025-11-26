# api/tests/helpers.py
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

def get_auth_client():
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        password='testpass'
    )
    client = APIClient()
    client.login(username='testuser', password='testpass')
    return client, user
