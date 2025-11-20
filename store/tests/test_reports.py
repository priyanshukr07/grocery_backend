from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Product, Category, User

class ReportsTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager", password="pass", role="manager"
        )
        self.client.force_authenticate(self.manager)

        cat = Category.objects.create(name="FRUITS")
        Product.objects.create(name="Apple", category=cat, price=10, stock=10)

    def test_sales_report(self):
        url = reverse("sales-by-product")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
