from django.shortcuts import render, HttpResponse
from Users.models import Level
from gamification.models import MissionProgress, QuizAttempt
from passport.models import ProductScan
import traceback
# Create your views here.
def home(request):
    '''
    Homepage for application
    Fetch user info from database and pass as context to display level, stats, etc.
    '''
    try:
        level = Level.objects.get(user=request.user).level
        points = Level.objects.get(user=request.user).points
    except Exception as e:
        level = None
        print(e)
        traceback.print_exc()
    missions_done = MissionProgress.objects.filter(
        user=request.user, 
        completed_at__isnull=False
    ).count()
    quizzes_attempted = QuizAttempt.objects.filter(user=request.user).count()
    products_scanned = ProductScan.objects.filter(user=request.user).count()
    try:
        last_scan = ProductScan.objects.filter(user=request.user).select_related('product').last()
    except:
        last_scan = None
    context = {
        'level': level,
        'points': points,
        'missions_done': missions_done,
        'quizzes_attempted': quizzes_attempted,
        'products_scanned': products_scanned,
        'last_scan': last_scan,
    }
    return render(request, 'home.html', context)

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
    return render(request, 'gamification/missions.html')

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
    return render(request, 'Users/signup.html')

def login(request):
    '''
    Allow user to log in
    '''
    return render(request, 'registration/login.html')

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