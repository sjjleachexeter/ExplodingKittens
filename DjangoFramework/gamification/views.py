import json
from http.client import responses

from django.contrib.auth.decorators import login_required
from django.contrib.messages.constants import SUCCESS
from django.core.checks import messages
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import render, redirect

from Users.decorators import game_manager_required
from gamification.models import Mission, MissionProgress, Quiz
from gamification.templates.gamification.forms import MissionForm, QuizForm


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

@game_manager_required
def dashboard(request):
    # get active missions
    active_missions = Mission.objects.filter(published=True)
    # get how many uses have started each mission
    active_missions = active_missions.annotate(in_progress_count=Count("progress",
                                                                       filter=Q(progress__started_at=None,
                                                                                _negated=True),
                                                                       distinct=True
                                                                       ))
    # get how many uses have finished each mission
    active_missions = active_missions.annotate(finished_count=Count("progress",
                                                                    filter=Q(progress__completed_at=None,
                                                                             _negated=True),
                                                                    distinct=True
                                                                    ))

    # get unpublished missions
    unpublished_missions = Mission.objects.filter(published=False)

    # get quiz's
    quizs = Quiz.objects.all()
    quizs = quizs.annotate(attempts_count=Count("attempts"))
    quizs = quizs.annotate(correct=Count("attempts",
                                         filter=Q(attempts__is_correct=True),
                                         distinct=True
                                         ))

    return render(request, 'gamification/dashboard.html',
                  {'active_missions': active_missions, 'unpublished_missions': unpublished_missions, 'quizs': quizs})


@game_manager_required
def publish_mission(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    mission.published = True
    mission.save()
    return redirect('dashboard')


@game_manager_required
def edit_mission(request, mission_id=None):
    mission = None
    try:
        mission = Mission.objects.get(id=mission_id)
    except Mission.DoesNotExist:
        pass
    if request.method == "POST":
        # check if this is a delete request
        if 'form-delete' in request.POST:
            if mission is not None:
                mission.delete()
            return redirect('dashboard')

        # create form with existing instance
        mission_form = MissionForm(request.POST, instance=mission)

        # update and return home is valid
        if mission_form.is_valid():
            mission_form.instance.mission_id = mission_form.instance.id
            mission_form.save()
            return redirect('dashboard')
    else:
        mission_form = MissionForm(instance=mission)

    return render(request, "gamification/edit_mission.html", {"mission_form": mission_form})


@game_manager_required
def edit_quiz(request, quiz_id=None):
    quiz_editing = None
    try:
        quiz_editing = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        pass
    if request.method == "POST":
        # check if this is a delete request
        if 'form-delete' in request.POST:
            if quiz_editing is not None:
                quiz_editing.delete()
            return redirect('dashboard')

        # create form with existing instance
        quiz_form = QuizForm(request.POST, instance=quiz_editing)

        # update and return home is valid
        if quiz_form.is_valid():
            quiz_form.instance.quiz_id = quiz_form.instance.id
            quiz_form.save()
            return redirect('dashboard')
    else:
        quiz_form = QuizForm(instance=quiz_editing)

    return render(request, "gamification/edit_quiz.html", {"quiz_form": quiz_form})
