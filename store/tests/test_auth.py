from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import User

class AuthTests(APITestCase):
    def test_register_customer(self):
        url = reverse("register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_login_jwt(self):
        User.objects.create_user(username="u1", password="Test@123")
        url = reverse("token_obtain_pair")
        data = {"username": "u1", "password": "Test@123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
