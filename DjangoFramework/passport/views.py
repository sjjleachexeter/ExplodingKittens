from django.shortcuts import render, redirect

from passport.models import Product


# Create your views here.

def return_to_scanner(request):
    response = redirect('/scan/')
    return response


def display_passport(request, product_id=-1):
    # try to load product
    try:
        product = Product.objects.get(product_id=product_id)
        context = {'product_id': product_id, 'passport_data': product}
        return render(request, "passport/passport.html", context)
    except Product.DoesNotExist:
        context = {'product_id': product_id}
        return render(request, "passport/passportNotExisting.html", context)



