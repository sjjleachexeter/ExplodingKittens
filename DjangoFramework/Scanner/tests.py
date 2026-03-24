from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from passport.models import ProductScan, Product

# Create your tests here.
class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("Scanner")

    def test_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Scanner/scan.html")

class TestLoadPassport(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("load_passport")
        self.user = User.objects.create_user(
            username='test_user',
            password='Password123!'
        )
        self.product = Product.objects.create(
            id=1,
            product_id=1,
            name='test',
            category=1,
            description='test',
            qr_token=1
        )

    def test_passport_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_passport_no_login(self):
        data = {
            'barcode': 1
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

    def test_passport_login(self):
        self.client.login(username='test_user', password='Password123!')
        data = {
            'barcode': 1
        }
        response = self.client.post(self.url, data)

        self.assertTrue(ProductScan.objects.filter(user=self.user).filter(product=self.product).exists())
        self.assertEqual(response.status_code, 302)