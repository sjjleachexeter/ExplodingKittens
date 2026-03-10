from django.test import TestCase, Client
from datetime import datetime
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Mission, MissionProgress, Quiz, QuizAttempt

# Create your tests here.
class TestMissionsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.missions_url = reverse("missions")

        self.user = User.objects.create_user(
            username = 'new test',
            password = 'Password123!'
        )

    def test_mission_no_login(self):
        response = self.client.get(self.missions_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/login_to_view.html')

    def test_mission_login(self):
        self.client.force_login(self.user)
        response = self.client.get(self.missions_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/missions.html')

class TestQuizView(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create(
            id = 1,
            mission_id = '1',

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = True
        )

        self.quiz = Quiz.objects.create(
            id = 1,
            quiz_id = '1',
            mission = self.mission,
            question = 'test question',
            choices = ['yes','no'],
            correct_choice_index = 0,
            explanation = 'test explanation'
        )

        self.mission = Mission.objects.create(
            id = 2,
            mission_id = '2',

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )

        self.quiz = Quiz.objects.create(
            id = 2,
            quiz_id = '2',
            mission = self.mission,
            question = 'test question',
            choices = ['yes','no'],
            correct_choice_index = 0,
            explanation = 'test explanation'
        )

        self.client = Client()
        self.quiz_url_no_quiz = reverse("quiz", args=['1913'])
        self.quiz_url = reverse("quiz", args=['1'])
        self.quiz_url_not_pub = reverse("quiz", args=['2'])

        self.user = User.objects.create_user(
            username = 'new test',
            password = 'Password123!'
        )

    def test_quiz_no_login(self):
        response = self.client.get(self.quiz_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/login_to_view.html')

    def test_quiz_no_quiz(self):
        self.client.force_login(self.user)
        response = self.client.get(self.quiz_url_no_quiz)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/quiz_does_not_exist.html')

    def test_quiz_published(self):
        self.client.force_login(self.user)
        response = self.client.get(self.quiz_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/quiz.html')

    def test_quiz_not_published(self):
        self.client.force_login(self.user)
        response = self.client.get(self.quiz_url_not_pub)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/quiz_does_not_exist.html')

class TestMissionsModel(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create(
            id = 1,
            mission_id = 1,

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )

    #Create
    def test_mission_create(self):
        self.assertTrue(Mission.objects.filter(id=1).exists())

    #Read
    def test_mission_read_id(self):
        self.assertEqual(self.mission.id, 1)

    def test_mission_read_mission_id(self):
        self.assertEqual(self.mission.mission_id, 1)

    def test_mission_read_title(self):
        self.assertEqual(self.mission.title, 'test')

    def test_mission_read_rules(self):
        self.assertEqual(self.mission.rules, {'test rule 1':'test rule'})

    def test_mission_read_points(self):
        self.assertEqual(self.mission.points, 10)

    def test_mission_read_description(self):
        self.assertEqual(self.mission.description, 'test description')

    def test_mission_read_example(self):
        self.assertEqual(self.mission.example, 'test example')

    def test_mission_read_learning_outcome(self):
        self.assertEqual(self.mission.learning_outcome, 'test outcome')

    def test_mission_read_start_at(self):
        self.assertEqual(self.mission.start_at, datetime(2026,1,10,5,0))

    def test_mission_read_end_at(self):
        self.assertEqual(self.mission.end_at, datetime(2026,1,20,5,0))

    #Update
    def test_mission_update_id(self):
        self.mission.id = 2

        self.assertTrue(Mission.objects.filter(id=1).exists())
        self.assertFalse(Mission.objects.filter(id=2).exists())

    def test_mission_update_mission_id(self):
        self.mission.mission_id = 2

        self.assertEqual(self.mission.mission_id, 2)

    def test_mission_update_title(self):
        self.mission.title = 'new'

        self.assertEqual(self.mission.title, 'new')

    def test_mission_update_rules(self):
        self.mission.rules = {'new':'new'}
        
        self.assertEqual(self.mission.rules, {'new':'new'})

    def test_mission_update_example(self):
        self.mission.example = 'new'

        self.assertEqual(self.mission.example, 'new')

    def test_mission_update_learning_outcome(self):
        self.mission.learning_outcome = 'new'

        self.assertEqual(self.mission.learning_outcome, 'new')

    def test_mission_update_start_at(self):
        self.mission.start_at = datetime(2026,1,12,5,0)

        self.assertEqual(self.mission.start_at, datetime(2026,1,12,5,0))

    def test_mission_update_end_at(self):
        self.mission.end_at = datetime(2026,1,12,5,0)

        self.assertEqual(self.mission.end_at, datetime(2026,1,12,5,0))
    
    def test_mission_update_published(self):
        self.mission.published = True

        self.assertEqual(self.mission.published, True)

    #Delete
    def test_mission_delete(self):
        self.mission.delete()

        self.assertFalse(Mission.objects.filter(id=1).exists())

    #constraints
    def test_mission_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.mission = Mission.objects.create(
                id = 1,
                mission_id = 2,

                title = "test 2",
                rules = {'test rule 2':'test rule'},
                points = 10,

                description = "test description 2",
                example = "test example 2",
                learning_outcome = "test outcome 2",

                start_at = datetime(2026,1,11,5,0),
                end_at = datetime(2026,1,21,5,0),
                published = False
                )
        
        self.assertEqual(Mission.objects.filter(id=1).count(), 1)

    def test_mission_mission_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.mission = Mission.objects.create(
                id = 2,
                mission_id = 1,

                title = "test 2",
                rules = {'test rule 2':'test rule'},
                points = 10,

                description = "test description 2",
                example = "test example 2",
                learning_outcome = "test outcome 2",

                start_at = datetime(2026,1,11,5,0),
                end_at = datetime(2026,1,21,5,0),
                published = False
                )

        self.assertEqual(Mission.objects.filter(mission_id=1).count(), 1)

    def test_mission_mission_id_length_1(self):
        mission_id = 'a' * 99
        self.mission.mission_id = mission_id
        self.mission.full_clean()

        self.assertEqual(self.mission.mission_id, mission_id)

    def test_mission_mission_id_length_2(self):
        mission_id = 'a' * 100
        self.mission.mission_id = mission_id
        self.mission.full_clean()

        self.assertEqual(self.mission.mission_id, mission_id)

    def test_mission_mission_id_length_3(self):
        mission_id = 'a' * 101
        self.mission.mission_id = mission_id

        with self.assertRaises(ValidationError):
            self.mission.full_clean()

    def test_mission_mission_id_length_4(self):
        mission_id = 'a' * 150
        self.mission.mission_id = mission_id
        
        with self.assertRaises(ValidationError):
            self.mission.full_clean()

    def test_mission_title_length_1(self):
        title = 'a' * 149
        self.mission.title = title
        self.mission.full_clean()

        self.assertEqual(self.mission.title, title)

    def test_mission_title_length_2(self):
        title = 'a' * 150
        self.mission.title = title
        self.mission.full_clean()

        self.assertEqual(self.mission.title, title)

    def test_mission_title_length_3(self):
        title = 'a' * 151
        self.mission.title = title
        with self.assertRaises(ValidationError):
            self.mission.full_clean()        
    
    def test_mission_title_length_4(self):
        title = 'a' * 200
        self.mission.title = title
        with self.assertRaises(ValidationError):
            self.mission.full_clean()

class TestMissionProgress(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create(
            id = 1,
            mission_id = 1,

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )

        self.user = User.objects.create_user(
            username = 'test',
            password = 'Password123!'
        )

        self.mission_progress = MissionProgress.objects.create(
            id = 1,
            mission = self.mission,

            user = self.user,

            started_at = datetime(2026,1,10,5,0),
            completed_at = datetime(2026,1,20,5,0),
            points_awarded = 10,
        )
        #re assigned to stop it automatically filling in the current time and date
        self.mission_progress.started_at = datetime(2026,1,10,5,0)

    #Create
    def test_mission_progress_create(self):
        self.assertTrue(MissionProgress.objects.filter(id=1).exists())

    #Read
    def test_mission_progress_read_id(self):
        self.assertEqual(self.mission_progress.id, 1)

    def test_mission_progress_read_mission(self):
        self.assertEqual(self.mission_progress.mission, self.mission)
    
    def test_mission_progress_read_user(self):
        self.assertEqual(self.mission_progress.user, self.user)

    def test_mission_progress_read_started_at(self):
        self.assertEqual(self.mission_progress.started_at, datetime(2026,1,10,5,0))

    def test_mission_progress_read_completed_at(self):
        self.assertEqual(self.mission_progress.completed_at, datetime(2026,1,20,5,0))

    def test_mission_progress_read_points_awarded(self):
        self.assertEqual(self.mission_progress.points_awarded, 10)

    #Update
    def test_mission_progress_update_id(self):
        self.mission_progress.id = 2

        self.assertTrue(MissionProgress.objects.filter(id=1).exists())
        self.assertFalse(MissionProgress.objects.filter(id=2).exists())

    def test_mission_progress_update_mission(self):
        mission = Mission.objects.create(
            id = 2,
            mission_id = 2,

            title = "test 2",
            rules = {'test rule 2':'test rule'},
            points = 10,

            description = "test description 2",
            example = "test example 2",
            learning_outcome = "test outcome 2",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )
        self.mission_progress.mission = mission

        self.assertEqual(self.mission_progress.mission, mission)

    def test_mission_progress_update_user(self):
        user = User.objects.create_user(
            username = 'test 2',
            password = 'Password123!'
        )
        self.mission_progress.user = user

        self.assertEqual(self.mission_progress.user, user)

    def test_mission_progress_update_started_at(self):
        self.mission_progress.started_at = datetime(2026,1,15,5,0)

        self.assertEqual(self.mission_progress.started_at, datetime(2026,1,15,5,0))

    def test_mission_progress_update_completed_at(self):
        self.mission_progress.completed_at = datetime(2026,1,15,5,0)

        self.assertEqual(self.mission_progress.completed_at, datetime(2026,1,15,5,0))

    def test_mission_progress_update_points_awarded(self):
        self.mission_progress.points_awarded = 20

        self.assertEqual(self.mission_progress.points_awarded, 20)

    #Delete
    def test_mission_progress_delete(self):
        self.mission_progress.delete()

        self.assertFalse(MissionProgress.objects.filter(id=1).exists())

    def test_mission_progress_delete_mission(self):
        self.mission.delete()

        self.assertFalse(MissionProgress.objects.filter(id=1).exists())

    def test_mission_progress_delete_user(self):
        self.user.delete()

        self.assertFalse(MissionProgress.objects.filter(id=1).exists())

    #Constraints
    def test_mission_progress_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.mission_progress = MissionProgress.objects.create(
                id = 1,
                mission = self.mission,

                user = self.user,

                started_at = datetime(2026,1,10,5,0),
                completed_at = datetime(2026,1,20,5,0),
                points_awarded = 10,
                )

class TestQuizModel(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create(
            id = 1,
            mission_id = 1,

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )

        self.quiz = Quiz.objects.create(
            id = 1,
            quiz_id = 1,
            mission = self.mission,
            question = 'test question',
            choices = ['yes','no'],
            correct_choice_index = 0,
            explanation = 'test explanation'
        )

    #Create
    def test_quiz_create(self):
        self.assertTrue(Quiz.objects.filter(id=1).exists())

    #Read
    def test_quiz_read_id(self):
        self.assertEqual(self.quiz.id, 1)

    def test_quiz_read_quiz_id(self):
        self.assertEqual(self.quiz.quiz_id, 1)

    def test_quiz_read_mission(self):
        self.assertEqual(self.quiz.mission, self.mission)

    def test_quiz_read_question(self):
        self.assertEqual(self.quiz.question, 'test question')
    
    def test_quiz_read_choices(self):
        self.assertEqual(self.quiz.choices, ['yes','no'])

    def test_quiz_read_correct_choice_index(self):
        self.assertEqual(self.quiz.correct_choice_index, 0)

    def test_quiz_read_explanation(self):
        self.assertEqual(self.quiz.explanation, 'test explanation')

    #Update
    def test_quiz_update_id(self):
        self.quiz.id = 2

        self.assertTrue(Quiz.objects.filter(id=1).exists())
        self.assertFalse(Quiz.objects.filter(id=2).exists())

    def test_quiz_update_quiz_id(self):
        self.quiz.quiz_id = 2

        self.assertEqual(self.quiz.quiz_id, 2)

    def test_quiz_update_mission(self):
        mission = Mission.objects.create(
            id = 2,
            mission_id = 2,

            title = "test 2",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description 2",
            example = "test example 2",
            learning_outcome = "test outcome 2",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )
        self.quiz.mission = mission

        self.assertEqual(self.quiz.mission, mission)

    def test_quiz_update_question(self):
        self.quiz.question = 'new'

        self.assertEqual(self.quiz.question, 'new')

    def test_quiz_update_choices(self):
        self.quiz.choices = ['1','2','3']

        self.assertEqual(self.quiz.choices, ['1','2','3'])

    def test_quiz_update_correct_choice_index(self):
        self.quiz.correct_choice_index = 1

        self.assertEqual(self.quiz.correct_choice_index, 1)
    
    def test_quiz_update_explanation(self):
        self.quiz.explanation = 'new'

        self.assertEqual(self.quiz.explanation, 'new')

    #Delete
    def test_quiz_delete(self):
        self.quiz.delete()

        self.assertFalse(Quiz.objects.filter(id=1).exists())

    def test_quiz_delete_mission(self):
        self.mission.delete()
        self.quiz.refresh_from_db()
        
        self.assertIsNone(self.quiz.mission)

    #Constraints
    def test_quiz_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.quiz = Quiz.objects.create(
                    id = 1,
                    quiz_id = 2,
                    mission = self.mission,
                    question = 'test question 2',
                    choices = ['yes','no'],
                    correct_choice_index = 0,
                    explanation = 'test explanation 2'
                )
    
    def test_quiz_quiz_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.quiz = Quiz.objects.create(
                    id = 2,
                    quiz_id = 1,
                    mission = self.mission,
                    question = 'test question 2',
                    choices = ['yes','no'],
                    correct_choice_index = 0,
                    explanation = 'test explanation 2'
                )

    def test_quiz_quiz_id_length_1(self):
        quiz_id = 'a' * 99
        self.quiz.quiz_id = quiz_id
        self.quiz.full_clean()

        self.assertEqual(self.quiz.quiz_id, quiz_id)

    def test_quiz_quiz_id_length_2(self):
        quiz_id = 'a' * 100
        self.quiz.quiz_id = quiz_id
        self.quiz.full_clean()

        self.assertEqual(self.quiz.quiz_id, quiz_id)

    def test_quiz_quiz_id_length_3(self):
        quiz_id = 'a' * 101
        self.quiz.quiz_id = quiz_id
        with self.assertRaises(ValidationError):
            self.quiz.full_clean()

    def test_quiz_quiz_id_length_4(self):
        quiz_id = 'a' * 150
        self.quiz.quiz_id = quiz_id
        with self.assertRaises(ValidationError):
            self.quiz.full_clean()

    #Methods
    def test_quiz_str(self):
        self.assertEqual(self.quiz.__str__(), 1)

class TestQuizAttempt(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create(
            id = 1,
            mission_id = 1,

            title = "test",
            rules = {'test rule 1':'test rule'},
            points = 10,

            description = "test description",
            example = "test example",
            learning_outcome = "test outcome",

            start_at = datetime(2026,1,10,5,0),
            end_at = datetime(2026,1,20,5,0),
            published = False
        )

        self.quiz = Quiz.objects.create(
            id = 1,
            quiz_id = 1,
            mission = self.mission,
            question = 'test question',
            choices = ['yes','no'],
            correct_choice_index = 0,
            explanation = 'test explanation'
        )

        self.user = User.objects.create_user(
            username = 'test',
            password = 'Password123!'
        )

        self.quiz_attempt = QuizAttempt.objects.create(
            id = 1,
            quiz = self.quiz,
            user = self.user,
            selected_choice_index = 0,
            is_correct = True,
            attempted_at = datetime(2026,1,20,5,0)
        )
        self.quiz_attempt.attempted_at = datetime(2026,1,20,5,0)

    #Create
    def test_quiz_attempt_create(self):
        self.assertTrue(QuizAttempt.objects.filter(id=1).exists())

    #Read
    def test_quiz_attempt_read_id(self):
        self.assertEqual(self.quiz_attempt.id, 1)

    def test_quiz_attempt_read_quiz(self):
        self.assertEqual(self.quiz_attempt.quiz, self.quiz)

    def test_quiz_attempt_read_user(self):
        self.assertEqual(self.quiz_attempt.user, self.user)

    def test_quiz_attempt_read_selected_choice_index(self):
        self.assertEqual(self.quiz_attempt.selected_choice_index, 0)

    def test_quiz_attempt_read_is_correct(self):
        self.assertEqual(self.quiz_attempt.is_correct, True)
    
    def test_quiz_attempt_read_attempted_at(self):
        self.assertEqual(self.quiz_attempt.attempted_at, datetime(2026,1,20,5,0))

    #Update
    def test_quiz_attempt_update_id(self):
        self.quiz_attempt.id = 2

        self.assertTrue(QuizAttempt.objects.filter(id=1).exists())
        self.assertFalse(QuizAttempt.objects.filter(id=2).exists())

    def test_quiz_attempt_update_quiz(self):
        quiz = Quiz.objects.create(
            id = 2,
            quiz_id = 2,
            mission = self.mission,
            question = 'test question 2',
            choices = ['yes','no'],
            correct_choice_index = 0,
            explanation = 'test explanation 2'
        )
        self.quiz_attempt.quiz = quiz

        self.assertEqual(self.quiz_attempt.quiz, quiz)

    def test_quiz_attempt_update_user(self):
        user = User.objects.create_user(
            username = 'test 2',
            password = 'Password123!'
        )
        self.quiz_attempt.user = user

        self.assertEqual(self.quiz_attempt.user, user)

    def test_quiz_attempt_update_selected_choice_index(self):
        self.quiz_attempt.selected_choice_index = 1
        
        self.assertEqual(self.quiz_attempt.selected_choice_index, 1)

    def test_quiz_attempt_update_is_correct(self):
        self.quiz_attempt.is_correct = False

        self.assertEqual(self.quiz_attempt.is_correct, False)

    def test_quiz_attempt_update_attempted_at(self):
        self.quiz_attempt.attempted_at = datetime(2026,1,25,5,0)

        self.assertEqual(self.quiz_attempt.attempted_at, datetime(2026,1,25,5,0))

    #Delete
    def test_quiz_attempt_delete(self):
        self.quiz_attempt.delete()

        self.assertFalse(QuizAttempt.objects.filter(id=1).exists())

    def test_quiz_attempt_delete_quiz(self):
        self.quiz.delete()

        self.assertFalse(QuizAttempt.objects.filter(id=1).exists())

    def test_quiz_attempt_delete_user(self):
        self.user.delete()

        self.assertFalse(QuizAttempt.objects.filter(id=1).exists())

    #Constraints
    def test_quiz_attempt_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.quiz_attempt = QuizAttempt.objects.create(
                    id = 1,
                    quiz = self.quiz,
                    user = self.user,
                    selected_choice_index = 0,
                    is_correct = True,
                    attempted_at = datetime(2026,1,20,5,0)
                )