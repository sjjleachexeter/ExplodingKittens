import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



# Create your views here.

def index(request):
    return render(request, "Scanner/scan.html")

def manual_editor(request):
    '''
    Will display the manual editor for the product passport
    '''
    return render(request, 'editor.html')
