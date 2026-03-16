import json

from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import render, redirect

from Users.decorators import game_manager_required
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

@game_manager_required
def dashboard(request):
    #get active missions
    active_missions = Mission.objects.filter(published = True)
    #get how many uses have started each mission
    active_missions = active_missions.annotate(in_progress_count=Count("progress",
                                filter=Q(progress__started_at=None, _negated=True),
                                distinct=True
                                ))
    # get how many uses have finished each mission
    active_missions = active_missions.annotate(finished_count=Count("progress",
                                                                 filter=Q(progress__completed_at=None, _negated=True),
                                                                 distinct=True
                                                                 ))

    unpublished_missions = Mission.objects.filter(published = False)

    return render(request, 'gamification/dashboard.html', {'active_missions': active_missions, 'unpublished_missions': unpublished_missions})


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = ['title', 'rules', 'points','description','example',
                  'learning_outcome','start_at','end_at','published']




@game_manager_required
def edit_mission(request, mission_id = None):
    mission = None
    try:
        mission = Mission.objects.get(id = mission_id)
    except Mission.DoesNotExist:
        pass
    if request.method == "POST":
        #check if this is a delete request
        if  'form-delete' in request.POST:
            if mission is not None:
                mission.delete()
                return redirect('dashboard')

        # create form with existing instance
        mission_form = MissionForm(request.POST, instance=mission)

        #update and return home is valid
        if mission_form.is_valid():
            mission_form.instance.mission_id = mission_form.instance.id
            mission_form.save()
            return redirect('dashboard')
    else:
        mission_form = MissionForm(instance=mission)

    return render(request, "gamification/edit_mission.html", {"mission_form": mission_form})

@game_manager_required
def publish_mission(request, mission_id):
    mission =  Mission.objects.get(id = mission_id)
    mission.published = True
    mission.save()
    return redirect('dashboard')