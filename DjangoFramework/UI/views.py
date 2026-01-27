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
    return render(request, 'scan.html')

def product_passport(request):
    '''
    Will display product passport page
    '''
    return render(request, 'product.html')

def missions(request):
    '''
    Display user missions (shows progress etc)
    '''
    return render(request, 'missions.html')

def leaderboard(request):
    '''
    Show leaderboard with user position (based on user points)
    '''
    return render(request, 'leaderboard.html')

def profile(request):
    '''
    Allow user to adjust personal & account settings
    '''
    return render(request, 'profile.html')

def user(request):
    '''
    Display information about a user
    '''
    return render(request, 'user.html')

def signup(request):
    '''
    Allow user to create an account
    '''
    return render(request, 'signup.html')

def login(request):
    '''
    Allow user to log in
    '''
    return render(request, 'login.html')

def privacy(request):
    '''
    Display privacy policy
    '''
    return render(request, 'privacy.html')

def terms(request):
    '''
    Display terms and conditions
    '''
    return render(request, 'terms.html')

def about(request):
    '''
    Display information about app (version etc.)
    '''
    return render(request, 'about.html')