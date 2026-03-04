from django.contrib.auth.models import User
from django.db.models import Count, Window, F, Q
from django.db.models.functions import RowNumber
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render
from django.template.context_processors import request

from Users.models import Level
from passport.models import ProductScan

fields = {
    "user": "name",
          "level": "level",
          "points": "points",
          "scans": "total scans",
          }
leaderboard_length = 50
# Create your views here.
def total_scans(user: User):
    return ProductScan.objects.filter(user=user).count()
def leaderboard(request):
    sort_by = request.GET.get('sort', '-level')
    # only accept available sorts
    if not sort_by.strip("-") in fields.keys():
        raise Http404("Node not found")
    # add user levels and points for the table
    table = Level.objects.all()
    # add user total scans for the table
    table = table.annotate(scans = Count("user__scans"))
    # remove private users and sort in correct order
    if request.user.is_authenticated:
        #keep the current user even if they are private only they see there place on the leaderboard
        table = table.filter( Q(user__leaderboard_preference__public=True) | Q(user=request.user)).order_by(sort_by)
    else:
        table = table.filter(user__leaderboard_preference__public=True).order_by(sort_by)

    # get the row of the current user
    user_row, user_position = None , None
    if request.user.is_authenticated:
        user_row = table.filter(user=request.user).get()
        # find the user_position of the user row in the sorted table
        field = sort_by.lstrip('-')
        is_desc = sort_by.startswith('-')
        value = getattr(user_row, field)
        if is_desc:
            user_position = table.filter(**{f"{field}__gt": value}).count() + 1
        else:
            user_position = table.filter(**{f"{field}__lt": value}).count() + 1
        # convert the users row into the same format as the rest
        user_row = [getattr(user_row, field) for field in fields]

    # convert into better format for the template and only keep the top 50
    table = [
        [getattr(row, field) for field in fields]
        for row in table[:leaderboard_length]
    ]
    # define rows in table
    return render(request, 'Leaderboard/leaderboard.html', {'table': table, 'fields': fields, 'sort_by': sort_by, 'user_row': user_row, 'user_position': user_position, 'leaderboard_length': leaderboard_length})
