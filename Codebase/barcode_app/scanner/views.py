import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



# Create your views here.

def index(request):
    return render(request, "scanner/index.html")

def scan_barcode(request):
    data = json.loads(request.body)
    barcode = data["barcode"]

    # process barcode (lookup product, etc.)
    return JsonResponse({"status": "ok", "barcode": barcode})
