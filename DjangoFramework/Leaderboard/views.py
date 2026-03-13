from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render

from Users.models import Level
from passport.models import ProductScan

# look up table for a database title to the name displayed on the webpage
fields = {
    "user": "name",
    "level": "level",
    "points": "points",
    "scans": "total scans",
    "completed_missions": "missions completed"
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

    table = get_table(request.user, sort_by)

    # get the row of the current user
    user_row, user_position = None, None
    if request.user.is_authenticated:
        user_row = table.filter(user=request.user).get()
        # find the user_position of the user row in the sorted table
        user_position = list(table).index(user_row) +1

    # convert into better format for the template
    table = [
        [getattr(row, field) for field in fields]
        for row in table[:leaderboard_length]
    ]
    # define rows in table
    return render(request, 'Leaderboard/leaderboard.html',
                  {'table': table, 'fields': fields, 'sort_by': sort_by, 'user_row': user_row,
                   'user_position': user_position, 'leaderboard_length': leaderboard_length})


def get_table(user, sort_by):
    """
    Aggregates all the data needed for the leaderboard table then sorts it into the correct order
    """
    # add user levels and points for the table
    table = Level.objects.all()
    # add total scans for the table
    table = table.annotate(scans=Count("user__scans"))
    # add completed missions to the table
    table = table.annotate(completed_missions=Count("user__mission_progress",
                                                    filter=Q(user__mission_progress__completed_at=None, _negated=True),
                                                    distinct=True
                                                    ))

    # remove private users and sort in correct order
    if user.is_authenticated:
        # keep the current user even if they are private only they see there place on the leaderboard
        table = table.filter(Q(user__leaderboard_preference__public=True) | Q(user=user)).order_by(sort_by)
    else:
        table = table.filter(user__leaderboard_preference__public=True).order_by(sort_by)

    return table