from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from .models import LeaderboardPreferences 


# Create your tests here.
class TestLeaderboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('leaderboard')

    def test_leaderboard(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Leaderboard/leaderboard.html")

class TestLeaderboardPreferences(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'new test',
            password = 'Password123!'
        )

        self.leaderboard_preferences = LeaderboardPreferences.objects.create(
            id = 1,
            user = self.user,
            public = False
        )
    
    #Create
    def test_leaderboard_preferences_create(self):
        self.assertTrue(LeaderboardPreferences.objects.filter(id=1).exists())

    #Read
    def test_leaderboard_preferences_read_id(self):
        self.assertEqual(self.leaderboard_preferences.id, 1)

    def test_leaderboard_preferences_read_user(self):
        self.assertEqual(self.leaderboard_preferences.user, self.user)

    def test_leaderboard_preferences_read_public(self):
        self.assertEqual(self.leaderboard_preferences.public, False)

    #Update
    def test_leaderboard_preferences_update_id(self):
        self.leaderboard_preferences.id = 2

        self.assertTrue(LeaderboardPreferences.objects.filter(id=1).exists())
        self.assertFalse(LeaderboardPreferences.objects.filter(id=2).exists())

    def test_leaderboard_preferences_update_user(self):
        user = User.objects.create(
            username = "new user",
            password = "Password123!"
        )
        self.leaderboard_preferences.user = user

        self.assertEqual(self.leaderboard_preferences.user, user)

    def test_leaderboard_preferences_update_public(self):
        self.leaderboard_preferences.public = True

        self.assertEqual(self.leaderboard_preferences.public, True)

    #Delete
    def test_leaderboard_preferences_delete(self):
        self.leaderboard_preferences.delete()

        self.assertFalse(LeaderboardPreferences.objects.filter(id=1).exists())

    def test_leaderboard_preferences_delete_user(self):
        self.user.delete()

        self.assertFalse(LeaderboardPreferences.objects.filter(id=1).exists())

    #Constraints
    def test_leaderboard_preferences_unique_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                leaderboard_preferences = LeaderboardPreferences.objects.create(
                    id = 1,
                    user = self.user,
                    public = False
                )

    #Methods
    def test_leaderboard_preferences_toggle_public_1(self):
        self.leaderboard_preferences.toggle_public()
        
        self.assertEqual(self.leaderboard_preferences.public, True)

    def test_leaderboard_preferences_toggle_public_2(self):
        self.leaderboard_preferences.public = True
        self.leaderboard_preferences.toggle_public()
        
        self.assertEqual(self.leaderboard_preferences.public, False)