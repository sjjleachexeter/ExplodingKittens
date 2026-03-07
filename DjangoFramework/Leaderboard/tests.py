from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class TestLeaderboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('leaderboard')

    def test_leaderboard(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Leaderboard/leaderboard.html")