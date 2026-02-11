from django.shortcuts import render, redirect

from passport.models import Product, ProductIngredient, Ingredient, Stage


# Create your views here.

def return_to_scanner(request):
    response = redirect('/scan/')
    return response


def display_passport(request, product_id=-1):
    # try to load product
    try:
        product = Product.objects.get(product_id=product_id)
        ingredients = ProductIngredient.objects.filter(product_id=product.id).select_related('ingredient').order_by('-proportion')
        stages = Stage.objects.filter(product=product.id).order_by('sequence')


        context = {'product_id': product_id, 'passport_data': product, "ingredients": ingredients, "stages": stages }
        return render(request, "passport/passport.html", context)
    except Product.DoesNotExist:
        # show error page if product does not exist
        context = {'product_id': product_id}
        return render(request, "passport/passportNotExisting.html", context)



