from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Category, User

class CategoryTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager", password="pass123", role="manager"
        )
        self.client.force_authenticate(self.manager)

    def test_create_category(self):
        url = reverse("categories-list")
        data = {"name": "FRUITS"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_category_slug_id(self):
        cat = Category.objects.create(name="FRUITS")
        url = reverse("category-details", args=[cat.slug, cat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
