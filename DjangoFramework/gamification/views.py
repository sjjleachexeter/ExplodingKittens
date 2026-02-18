import json

from django.shortcuts import render

from gamification.models import Mission, MissionProgress, Quiz


# Create your views here.


def missions(request):
    if request.user.is_authenticated:
        available_missions = Mission.objects.filter(published = True)
        progress = MissionProgress.objects.filter(user = request.user)


        context = {'missions': available_missions, 'progress': progress}
        return render(request, 'gamification/missions.html', context)

    return render(request, 'gamification/login_to_view.html')


def quiz(request, quiz_id):
    if request.user.is_authenticated:
        try:
            quiz_data = Quiz.objects.filter(quiz_id = quiz_id).get()
            if not quiz_data.mission.published:
                raise Exception("quiz not published")
            context = {'quiz_data': quiz_data}
            return render(request, 'gamification/quiz.html', context)
        except:
            return render(request, 'gamification/quiz_does_not_exist.html')

    return render(request, 'gamification/login_to_view.html')
