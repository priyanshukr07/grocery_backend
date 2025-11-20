from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Product, Category, User

class ProductTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager", password="pass123", role="manager"
        )
        self.client.force_authenticate(self.manager)

        self.category = Category.objects.create(name="FRUITS")

    def test_create_product(self):
        url = reverse("products-list")
        data = {
            "name": "Apple",
            "category_id": self.category.id,
            "price": "50.00",
            "stock": 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_product_slug_id(self):
        product = Product.objects.create(name="Apple", category=self.category, price=50, stock=5)
        url = reverse("product-details", args=[product.slug, product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
