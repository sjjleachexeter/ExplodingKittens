import json
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from passport.models import ProductScan, Product


# Create your views here.

def index(request):
    return render(request, "Scanner/scan.html")


def load_passport(request):
    if request.method == "POST":
        barcode = request.POST.get("barcode")
        # if the user is logged in add this to there scanned list
        if request.user.is_authenticated:
            print("user is logged in")
            try:
                product = Product.objects.get(qr_token=barcode)
                ProductScan.objects.update_or_create(
                    user=request.user,
                    product=product,
                    defaults={
                        "product": product,
                        "user": request.user,
                    },
                )

            except Product.DoesNotExist:
                # invalid product so do not add to users scans
                pass

        return redirect(reverse('passport_display', kwargs={'product_id': barcode}))
    else:
        raise Http404("Node not found")

