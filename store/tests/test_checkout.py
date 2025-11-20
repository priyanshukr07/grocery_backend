from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Product, Category, User

class CheckoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass")
        self.client.force_authenticate(self.user)

        cat = Category.objects.create(name="FRUITS")
        self.product = Product.objects.create(name="Apple", category=cat, price=50, stock=10)

        # add cart item
        self.client.post(reverse("cart-list"), {"product_id": self.product.id, "quantity": 2})

    def test_checkout(self):
        url = reverse("cart-checkout")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)
