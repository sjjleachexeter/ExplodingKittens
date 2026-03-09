from django.contrib.auth import forms
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from passport.forms import ProductForm, IngredientFormSet, StageFormSet, EditProductForm, ClaimFormSet, EvidenceFormSet, \
    NodeForm
from passport.models import Product, ProductIngredient, Stage, Node


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


@permission_required("passport.ProductAdmin")
def create_node(request, node_id = None):
    try:
        node = Node.objects.get(node_id=node_id)
    except Node.DoesNotExist:
        node = None
    if request.method == "POST" and 'form-delete' in request.POST:
        node.delete()
        return redirect('home')
    if request.method == "POST":
        node_form = NodeForm(request.POST)

        if node_form.is_valid():
            node_form.instance.node_id = node_form.instance.id
            node_form.save()

            return redirect(
                reverse('node_info_display', kwargs={'node_id': node_form.instance.node_id})
            )
    else :

        node_form = NodeForm(instance = node)

    return render(request,"passport/edit_node.html", {"node_form": node_form})


@permission_required("passport.ProductAdmin")
def create_passport(request):
    # check for delete post
    if request.method == "POST" and 'form-delete' in request.POST:
        # don't save anything and just go back home
        return redirect('home')
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST)
        stage_formset = StageFormSet(request.POST)

        if product_form.is_valid() and ingredient_formset.is_valid() and stage_formset.is_valid():
            # load product
            product = product_form.save(commit=False)
            # add product_id (same as qr_token)
            product.product_id = product.qr_token
            product.save()
            saved_product = Product.objects.get(product_id=product.qr_token)

            ingredient_formset.instance = saved_product
            ingredient_formset.save()

            stage_formset.instance = saved_product
            for (i, form) in enumerate(stage_formset.forms):
                form.instance.stage_id = form.instance.id
                form.instance.sequence = i
            stage_formset.save()

            # send user to product on success
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
        stage_formset = StageFormSet()
        return render(request, "passport/edit_passport.html", {
            "product_form": product_form,
            "ingredient_formset": ingredient_formset,
            "stage_formset": stage_formset
        })


@permission_required("passport.ProductAdmin")
def edit_passport(request, product_id):
    product = Product.objects.get(product_id=product_id)
    # check for delete post
    if request.method == "POST" and 'form-delete' in request.POST:
        # remove product from database
        product.delete()
        return redirect('home')
    # see if there is the form is valid and if so save the updated product
    if request.method == "POST":
        product_form = EditProductForm(request.POST, instance=product)
        ingredient_formset = IngredientFormSet(request.POST, instance=product)
        stage_formset = StageFormSet(request.POST, instance=product)

        if product_form.is_valid() and ingredient_formset.is_valid() and stage_formset.is_valid():
            product_form.save()

            ingredient_formset.instance = product
            ingredient_formset.save()

            stage_formset.instance = product
            for (i, form) in enumerate(stage_formset.forms):
                form.instance.stage_id = form.instance.id
                form.instance.sequence = i
            stage_formset.save()

            # send user to product on success
            return redirect(
                reverse('passport_display', kwargs={'product_id': product.qr_token})
            )

    else:
        product_form = EditProductForm(instance=product)
        ingredient_formset = IngredientFormSet(instance=product)
        stage_formset = StageFormSet(instance=product)

    return render(request, "passport/edit_passport.html", {
        "product_form": product_form,
        "ingredient_formset": ingredient_formset,
        "stage_formset": stage_formset
    })


@permission_required("passport.ProductAdmin")
def edit_claims(request, product_id):
    product = Product.objects.get(product_id=product_id)
    # check for delete post

    # see if there is the form is valid and if so save the updated product
    if request.method == "POST":
        claims_form = ClaimFormSet(request.POST, instance=product)

        if claims_form.is_valid():
            claims_form.instance = product
            # use default ids
            for claim in claims_form.forms:
                claim.instance.claim_id = claim.instance.id
                # update evidence to be linked to the same stage as the claim
                if len(claim.instance.claim_evidence_links.all()) != 0:
                    for link in claim.instance.claim_evidence_links.all():
                        evidence = link.evidence
                        evidence.stage_id = claim.instance.stage_id
                        evidence.stage = claim.instance.stage
                        evidence.scope = "stage"
                        evidence.save()
                else:
                    claim.instance.missing_evidence = True
                    claim.save()

            claims_form.save()

            # send user to product on success
            return redirect(
                reverse('passport_display', kwargs={'product_id': product.qr_token})
            )

    else:
        # create formset for claims about the product
        claims_form = ClaimFormSet(instance=product)

    return render(request, "passport/edit_claims.html", {"claims_form": claims_form})


@permission_required("passport.ProductAdmin")
def edit_evidence(request, product_id):
    product = Product.objects.get(product_id=product_id)
    # check for delete post

    # see if there is the form is valid and if so save the updated product
    if request.method == "POST":
        evidences_form = EvidenceFormSet(request.POST, instance=product)

        if evidences_form.is_valid():
            evidences_form.instance = product
            # use default ids and set scope
            for form in evidences_form.forms:
                form.instance.evidence_id = form.instance.id

            evidences_form.save()

            # send user to product on success
            return redirect(
                reverse('passport_display', kwargs={'product_id': product.qr_token})
            )

    else:
        # create formset for claims about the product
        evidences_form = EvidenceFormSet(instance=product)

    return render(request, "passport/edit_evidence.html", {"evidences_form": evidences_form})
