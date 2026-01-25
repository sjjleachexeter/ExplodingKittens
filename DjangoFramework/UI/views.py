from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    '''
    Homepage for application
    '''
    return render(request, 'home.html')

def scan(request):
    '''
    Scanner functionality is implemented on its own page
    Avoids broken behaviour being displayed on home page if camera unavailable'''
    return HttpResponse("Scan page")

def product_passport(request):
    '''
    Will display product passport page
    '''
    return HttpResponse("Product passport")

def missions(request):
    '''
    Display user missions (shows progress etc)
    '''
    return HttpResponse("Missions")

def leaderboard(request):
    '''
    Show leaderboard with user position (based on user points)
    '''
    return HttpResponse("Leaderboard")

def profile(request):
    '''
    Allow user to adjust personal & account settings
    '''
    return HttpResponse("User's own profile")

def user(request):
    '''
    Display information about a user
    '''
    return HttpResponse("Profile of another user")

def signup(request):
    '''
    Allow user to create an account
    '''
    return HttpResponse("Signup page")

def login(request):
    '''
    Allow user to log in
    '''
    return HttpResponse("Login page")

def privacy(request):
    '''
    Display privacy policy
    '''
    return HttpResponse("Privacy Policy")

def terms(request):
    '''
    Display terms and conditions
    '''
    return HttpResponse("Terms and Conditions")

def about(request):
    '''
    Display information about app (version etc.)
    '''
    return HttpResponse("Site info.")