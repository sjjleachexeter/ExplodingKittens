import json

import pandas as pd
import os

from gamification.models import Mission, Quiz

# define csv file location
csv_missions = "gamification/initialData/missions.csv"
csv_quizzes = "gamification/initialData/quizzes.csv"


def load_csv_missions():
    df = pd.read_csv(csv_missions)

    for index, row in df.iterrows():
        Mission.objects.update_or_create(
            mission_id=row['mission_id'],
            defaults={
                "title": row['title'],
                "rules": json.loads(row['rules']),
                "points": row['points'],
                "start_at": None if pd.isna(row['start_at']) else row['start_at'],
                "end_at": None if pd.isna(row['end_at']) else row['end_at'],
                "published": row['published'],
            }
        )


def load_csv_quizzes():
    df = pd.read_csv(csv_quizzes)

    for index, row in df.iterrows():
        Quiz.objects.update_or_create(
            quiz_id=row['quiz_id'],  # lookup by unique field
            defaults={
                'mission': Mission.objects.get(mission_id=row['mission_id']),
                'question': row['question'],
                'choices': json.loads(row['choices']),
                'correct_choice_index': row['correct_choice_index'],
                'explanation': row['explanation'],
            }
        )


def run():
    load_csv_missions()
    load_csv_quizzes()
