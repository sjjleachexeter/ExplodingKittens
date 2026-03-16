from django.forms import ModelForm

from gamification.models import Mission, Quiz


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = ['title', 'rules', 'points','description','example',
                  'learning_outcome','start_at','end_at','published']


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['mission', 'question','choices','correct_choice_index','explanation']
