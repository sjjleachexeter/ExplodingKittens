from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class TestHome(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

class TestProductPassport(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('product')

    def test_product_passport(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product.html")

class TestLeaderboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('leaderboard')

    def test_leaderboard(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leaderboard.html")

class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')

    def test_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

class TestUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user')

    def test_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user.html")

class TestPrivacy(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('privacy')

    def test_privacy(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "privacy.html")

class TestTerms(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('terms')

    def test_terms(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "terms.html")

class TestAbout(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('about')

    def test_about(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")