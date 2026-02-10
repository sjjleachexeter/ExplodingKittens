import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



# Create your views here.

def index(request):
    return render(request, "Scanner/scan.html")
