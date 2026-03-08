from django.contrib.auth import forms
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from passport.models import Product, ProductIngredient, Ingredient, Stage, Node


# Create your views here.

def return_to_scanner(request):
    response = redirect('/scan/')
    return response


def display_passport(request, product_id=-1):
    # try to load product
    try:
        product = Product.objects.get(product_id=product_id)
        ingredients = ProductIngredient.objects.filter(product_id=product.id).select_related('ingredient').order_by(
            '-proportion')
        stages = Stage.objects.filter(product=product.id).order_by('sequence')

        context = {'product_id': product_id, 'passport_data': product, "ingredients": ingredients, "stages": stages}
        return render(request, "passport/passport.html", context)
    except Product.DoesNotExist:
        # show error page if product does not exist
        context = {'product_id': product_id}
        return render(request, "passport/passportNotExisting.html", context)


def display_node_info(request, node_id=-1):
    try:
        node = Node.objects.get(node_id=node_id)
        context = {'node': node}
        return render(request, "passport/node_info.html", context)

    except Node.DoesNotExist:
        raise Http404("Node not found")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'qr_token']


class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description']


class ProductIngredientForm(ModelForm):
    class Meta:
        model = ProductIngredient
        fields = ['ingredient', 'proportion', 'origin_country']


IngredientFormSet = inlineformset_factory(
    Product,
    ProductIngredient,
    form=ProductIngredientForm,
    extra=1,
    can_delete=True
)


@permission_required("passport.ProductAdmin")
def create_passport(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST)



        if product_form.is_valid() and ingredient_formset.is_valid():
            # load product
            product = product_form.save(commit=False)
            # add product_id (same as qr_token)
            product.product_id = product.qr_token
            product.save()



            ingredient_formset.instance = Product.objects.get(product_id=product.qr_token)
            ingredient_formset.save()

            return redirect(
                reverse('passport_display', kwargs={'product_id': product.qr_token})
            )

        # return the form if it's wrong
        return render(request, "passport/edit_passport.html", {
            "product_form": product_form,
            "ingredient_formset": ingredient_formset
        })

    else:
        product_form = ProductForm()
        ingredient_formset = IngredientFormSet()
        return render(request, "passport/edit_passport.html", {"product_form": product_form, "ingredient_formset": ingredient_formset})


@permission_required("passport.ProductAdmin")
def edit_passport(request, product_id):
    product = Product.objects.get(product_id=product_id)

    if request.method == "POST":

        product_form = EditProductForm(request.POST, instance=product)
        ingredient_formset = IngredientFormSet(request.POST, instance=product)

        if product_form.is_valid() and ingredient_formset.is_valid():
            product_form.save()

            ingredient_formset.instance = product
            ingredient_formset.save()

            return redirect(
                reverse('passport_display', kwargs={'product_id': product.qr_token})
            )

    else:

        product_form = EditProductForm(instance=product)
        ingredient_formset = IngredientFormSet(instance=product)

    return render(request, "passport/edit_passport.html", {
        "product_form": product_form,
        "ingredient_formset": ingredient_formset
    })
