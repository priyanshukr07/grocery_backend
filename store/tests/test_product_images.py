from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import Product, Category, User

class ProductImageTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="manager", password="pass123", role="manager")
        self.client.force_authenticate(self.manager)

        cat = Category.objects.create(name="FRUITS")
        self.product = Product.objects.create(name="Apple", category=cat, price=10, stock=10)

    def test_upload_product_image(self):
        url = reverse("product-images-list-create", args=[self.product.id])
        img = SimpleUploadedFile("test.jpg", b"image_data", content_type="image/jpeg")
        response = self.client.post(url, {"images": img}, format="multipart")
        self.assertEqual(response.status_code, 201)
