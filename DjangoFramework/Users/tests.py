from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class TestAccounts(TestCase):
    def setUp(self):
        self.client = Client()
        self.accounts_url = reverse('accounts')

    def test_accounts(self):
        response = self.client.get(self.accounts_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/accounts.html")

class TestSignup(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup(self):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/signup.html")
    
    def test_signup_create_user(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "testuser",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_signup_create_user_wrong_password(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser",
                "password1": "Password123!",
                "password2": "WrongPassword",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser").exists())
        self.assertContains(response, "password")
    
    def test_signup_create_user_long_username1(self):
        username = 'a' * 200
        response = self.client.post(
            self.signup_url,
            data={
                "username": username,
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertContains(response, "username")

    def test_signup_create_user_long_username2(self):
        username = 'a' * 151
        response = self.client.post(
            self.signup_url,
            data={
                "username": username,
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertContains(response, "username")
    
    def test_signup_create_user_long_username3(self):
        username = 'a' * 150
        response = self.client.post(
            self.signup_url,
            data={
                "username": username,
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_signup_create_user_long_username4(self):
        username = 'a' * 149
        response = self.client.post(
            self.signup_url,
            data={
                "username": username,
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_signup_create_user_invalid_characters_username(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser$",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser$").exists())
        self.assertContains(response, "username")

    def test_signup_create_user_similar_information_password(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser",
                "password1": "wronguser",
                "password2": "wronguser",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser").exists())
        self.assertContains(response, "username")

    def test_signup_create_user_short_password(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser",
                "password1": "Pass",
                "password2": "Pass",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser").exists())
        self.assertContains(response, "username")

    def test_signup_create_user_numeric_password(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser",
                "password1": "123",
                "password2": "123",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser").exists())
        self.assertContains(response, "username")

    def test_signup_create_user_common_password(self):
        response = self.client.post(
            self.signup_url,
            data={
                "username": "wronguser",
                "password1": "Password",
                "password2": "Password",
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="wronguser$").exists())
        self.assertContains(response, "username")

    def test_signup_create_same_user(self):
        self.user = User.objects.create_user(
            username = 'test',
            password = 'Password123!'
        )

        response = self.client.post(
            self.signup_url,
            data={
                "username": "test",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="test").count(), 1)
        self.assertContains(response, "username")

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = "/accounts/login/"
        
        self.user = User.objects.create_user(
            username = 'test',
            password = 'Password123!'
        )

    def test_login(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_successful(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "test",
                "password": "Password123!",
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "test",
                "password": "wrongpassword",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password')

    def test_login_wrong_username(self):
        response = self.client.post(
            self.login_url,
            data={
                "username": "wrongname",
                "password": "Password123!",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')