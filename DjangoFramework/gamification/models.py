import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Mission(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    mission_id = models.CharField(max_length = 100, unique = True)

    title = models.CharField(max_length = 150)
    rules = models.JSONField(default =dict)
    points = models.IntegerField(default = 50)

    description = models.TextField(blank=True)
    example = models.TextField(blank=True)
    learning_outcome = models.TextField(blank=True)

    start_at = models.DateTimeField(null = True, blank = True)
    end_at =models.DateTimeField(null =True, blank = True)
    published = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class MissionProgress(models.Model):
    id = models.UUIDField(primary_key =True, default = uuid.uuid4, editable = False)
    mission = models.ForeignKey(Mission, on_delete = models.CASCADE, related_name = "progress")
    #connect to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mission_progress")

    started_at = models.DateTimeField(auto_now_add = True)
    completed_at = models.DateTimeField(null = True, blank = True)
    points_awarded = models.IntegerField(default = 0)


class Quiz(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    quiz_id = models.CharField(max_length = 100, unique = True)
    mission = models.ForeignKey(Mission, on_delete = models.SET_NULL, null = True, blank = True, related_name = "quizzes")
    question = models.TextField()
    choices = models.JSONField(default = list)
    correct_choice_index = models.PositiveSmallIntegerField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.quiz_id


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    quiz = models.ForeignKey(Quiz, on_delete =models.CASCADE, related_name = "attempts")
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "quiz_attempts")
    selected_choice_index = models.PositiveSmallIntegerField()
    is_correct = models.BooleanField(default = False)
    attempted_at = models.DateTimeField(auto_now_add = True)
