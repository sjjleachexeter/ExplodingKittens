from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("Scanner")

    def test_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Scanner/scan.html")