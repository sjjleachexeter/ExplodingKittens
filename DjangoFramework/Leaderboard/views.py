from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import render

from Users.models import Level
from passport.models import ProductScan


# Create your views here.
def total_scans(user: User):
    return ProductScan.objects.filter(user=user).count()
def leaderboard(request):
    sort_by = request.GET.get('sort', 'scans')
    fields = ["user", "level", "points", "scans"]
    # add user levels and points for the table
    table = Level.objects.all()
    # add user total scans for the table
    table = table.annotate(scans = Count("user__scans"))
    # remove private users and sort in correct order
    table = table.filter(user__leaderboard_preference__public=True).order_by(sort_by)


    table = [
        [getattr(row, field) for field in fields]
        for row in table
    ]
    # define rows in table
    return render(request, 'Leaderboard/leaderboard.html', {'table': table, 'fields': fields, 'sort_by': sort_by})
