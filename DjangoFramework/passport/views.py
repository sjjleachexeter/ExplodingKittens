from django.shortcuts import render, redirect


# Create your views here.

def return_to_scanner(request):
    response = redirect('/scan/')
    return response
def display_passport(request, product_id = -1):
    return render(request, "passport/passport.html", {"product_id": product_id})
