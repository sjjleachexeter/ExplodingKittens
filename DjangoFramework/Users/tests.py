from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from .models import Level, Types
from Leaderboard.models import LeaderboardPreferences

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

class TestDeleteAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('delete_account')

    def test_delete_account_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
    
    def test_delete_account_logged_in(self):
        user = User.objects.create_user(
            username = 'test_user',
            password = 'Password123!'
        )
        self.client.login(username = 'test_user', password = 'Password123!')
        response = self.client.post(self.url)

        self.assertFalse(User.objects.filter(username='test_user').exists())
        self.assertEqual(response.status_code, 302)

class TestLogoutAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout_account')
        self.user = User.objects.create_user(
            username = 'test_user',
            password = 'Password123!'
        )

    def test_logout_account_no_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_logout_account_login(self):
        self.client.login(username = 'test_user', password = 'Password123!')
        response = self.client.post(self.url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 302)

class TestPublicAccount(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'test_user',
            password = 'Password123!'
        )

        self.leaderboard_preferences = LeaderboardPreferences.objects.create(
            id = 1,
            user = self.user,
            public = False
        )

        self.client = Client()
        self.url = reverse('public_account')

    def test_public_account_no_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_public_account_login(self):
        self.client.login(username = 'test_user', password = 'Password123!')
        response = self.client.post(self.url)
        self.leaderboard_preferences.refresh_from_db()

        self.assertEqual(self.leaderboard_preferences.public, True)
        self.assertEqual(response.status_code, 302)

class TestEditRoles(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('edit_roles')

        self.superuser = User.objects.create_superuser(
            username='test_superuser',
            password='Password123!'
        )

        self.user = User.objects.create_user(
            username='test_user',
            password='Password1231'
        )
    
    def test_edit_roles_no_loggin(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_edit_roles_user(self):
        self.client.login(username='test_user', password='Password123!')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_edit_roles_superuser_get(self):
        self.client.login(username='test_superuser', password='Password123!')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/edit_roles.html")

    def test_edit_roles_superuser_post(self):
        self.client.login(username='test_superuser', password='Password123!')
        post_data = {
            'user': self.user.id,
            'type': Types.Roles.MANAGER
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)

    def test_edit_roles_bad_form(self):
        self.client.login(username='test_superuser', password='Password123!')
        post_data = {
            'user': self.user.id,
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/edit_roles.html")

class TestLevel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='new_test_user',
            password='Password123!'
        )

        self.level = self.user.current_level
        self.level.user=self.user
        self.level.level=5
        self.level.points=100

    #Create
    def test_level_create(self):
        self.assertTrue(Level.objects.filter(id=self.level.id).exists())

    #Read
    # def test_level_read_id(self):
    #     self.assertEqual(self.level.id, 1)

    def test_level_read_user(self):
        self.assertEqual(self.level.user, self.user)

    def test_level_read_level(self):
        self.assertEqual(self.level.level, 5)

    def test_level_read_points(self):
        self.assertEqual(self.level.points, 100)

    #Update
    def test_level_update_id(self):
        self.level.id = 2

        self.assertFalse(Level.objects.filter(id=2).exists())

    def test_level_update_user(self):
        user = User.objects.create_user(
            username='new_user',
            password='Password123!'
        )
        self.level.user = user

        self.assertEqual(self.level.user, user)

    def test_level_update_level(self):
        self.level.level = 10
        
        self.assertEqual(self.level.level, 10)

    def test_level_update_points(self):
        self.level.points = 200

        self.assertEqual(self.level.points, 200)

    #Delete
    def test_level_delete(self):
        self.level.delete()

        self.assertFalse(Level.objects.filter(user=self.user).exists())

    def test_level_delete_user(self):
        id = self.level.id
        self.user.delete()

        self.assertFalse(Level.objects.filter(id=id).exists())

    #Constraints
    def test_level_id_unique(self):
        id = self.level.id
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                level = Level.objects.create(
                    id = id,
                    user = self.user,
                    level = 10,
                    points = 150
                )

    def test_level_defaults(self):
        user = User.objects.create_user(
            username='new_user',
            password='Password123!'
        )

        self.assertEqual(user.current_level.level, 1)
        self.assertEqual(user.current_level.points, 0)

    #Methods
    def test_level_str(self):
        self.assertEqual(self.level.__str__(), "new_test_user - Level 5")

    def test_level_update(self):
        self.level.update_level()

        self.assertEqual(self.level.level, 2)

class TestTypes(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='Password123!'
        )
        
        self.types = self.user.role

    #Create
    def test_types_create(self):
        self.assertTrue(Types.objects.filter(user=self.user).exists())

    #Read
    def test_types_read_type(self):
        self.assertEqual(self.types.type, Types.Roles.GEN_USER)

    def test_types_read_user(self):
        self.assertEqual(self.types.user, self.user)

    #Update
    def test_types_update_type(self):
        self.types.type = Types.Roles.MANAGER

        self.assertEqual(self.types.type, Types.Roles.MANAGER)

    def test_types_update_user(self):
        user = User.objects.create_user(
            username='new_user',
            password='Password123!'
        )
        self.types.user = user

        self.assertEqual(self.types.user, user)

    #Delete
    def test_types_delete(self):
        self.types.delete()

        self.assertFalse(Types.objects.filter(user=self.user).exists())

    def test_types_delete_user(self):
        self.user.delete()
        
        if self.types:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    #Methods
    def test_types_str(self):
        self.assertEqual(self.types.__str__(), 'test_user - GEN_USER')
