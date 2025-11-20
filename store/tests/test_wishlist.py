from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Product, Category, User

class WishlistTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass")
        self.client.force_authenticate(self.user)

        cat = Category.objects.create(name="FRUITS")
        self.product = Product.objects.create(name="Apple", category=cat, price=50, stock=10)

    def test_add_wishlist(self):
        url = reverse("wishlist-list")
        data = {"product_id": self.product.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
