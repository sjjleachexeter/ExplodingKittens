import json
from http.client import responses

from django.contrib.auth.decorators import login_required
from django.contrib.messages.constants import SUCCESS
from django.core.checks import messages
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect

from gamification.models import Mission, MissionProgress, Quiz


# Create your views here.

def missions(request):
    if request.user.is_authenticated:
        available_missions = Mission.objects.filter(published=True).prefetch_related(
            Prefetch(
                "progress",  # related_name from MissionProgress
                queryset=MissionProgress.objects.filter(user=request.user),
                to_attr="user_progress"
            ))
        progress = MissionProgress.objects.filter(user=request.user)

        context = {'missions': available_missions, 'progress': progress}
        return render(request, 'gamification/missions.html', context)

    return render(request, 'gamification/login_to_view.html')

@login_required
def quiz(request, quiz_id):
    if request.user.is_authenticated:
        try:
            quiz_data = Quiz.objects.filter(quiz_id=quiz_id).get()
            if not quiz_data.mission.published:
                raise Exception("quiz not published")
            context = {'quiz_data': quiz_data}
            return render(request, 'gamification/quiz.html', context)
        except:
            return render(request, 'gamification/quiz_does_not_exist.html')

    return render(request, 'gamification/login_to_view.html')


@login_required
def start_mission(request):
    if request.method == "POST":
        user = request.user
        mission_id = request.POST['mission_id']
        # see if the mission is already in progress

        if not Mission.objects.filter(id=mission_id, published=True).exists() or MissionProgress.objects.filter(
                user=user, mission_id=mission_id).exists():
            # this is an invalid request
            raise Http404("Invalid mission request")

        MissionProgress.objects.create(user=user, mission_id=mission_id)
        return redirect(missions)
    return None


@login_required
def take_quiz(request):
    if request.method == "POST":
        user = request.user
        mission_id = request.POST['mission_id']
        print("help")
        if not Mission.objects.filter(id=mission_id, published=True).exists():
            # this is an invalid request
            raise Http404("Invalid mission request")
        # find quiz for the user to complete that they have not gotten right
        mission = Mission.objects.filter(id=mission_id, published=True).get()
        test = Quiz.objects.filter(mission=mission)
        for available_quiz in test:
            if available_quiz.attempts.filter(user=user, is_correct=True).exists():
                continue
            return redirect("quiz", quiz_id=available_quiz.quiz_id)

        # there are no more quiz's for the user to take
        raise Http404("No quiz's available")
    return None