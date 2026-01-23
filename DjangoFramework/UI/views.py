from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    '''
    Homepage for application, probably where scanner is integrated (tho scanner could have own page too?)
    '''
    return render(request, 'home.html')

def product_passport(request):
    '''
    Will display product passport page
    '''

def missions(request):
    '''
    Display user missions (shows progress etc)
    '''

def leaderboard(resuest):
    '''
    shows leaderboard with user position (based on user points)
    '''

def auth(request):
    '''
    possible authentication page
    '''

def about(request):
    '''
    gives app info? Might include links to T&Cs/privacy policy
    '''

def profile(request):
    '''
    where user can adjust personal settings and stuff
    '''