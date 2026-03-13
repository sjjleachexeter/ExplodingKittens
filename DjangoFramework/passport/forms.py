from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet, formset_factory
from numpy.ma.core import product

from passport.models import Product, ProductIngredient, Stage, Claim, Evidence, ClaimEvidence, Node, Ingredient


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ['org_name', 'role', 'country', 'city']

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


class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['stage_name', 'from_node', 'to_node', 'value_share', 'date_start', 'date_end']


StageFormSet = inlineformset_factory(
    Product,
    Stage,
    form=StageForm,
    extra=1,
    can_delete=True,
)


class ClaimForm(ModelForm):
    class Meta:
        model = Claim
        fields = ['stage', 'claim_type', 'statement', 'evidence']

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            self.fields['stage'].queryset = Stage.objects.filter(product=product)
            self.fields['evidence'].queryset = Evidence.objects.filter(product=product)



# override base set so we can filter and only show stages / claims relevant to the product
class BaseProductDerivativeFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['product'] = self.instance  # the Product instance
        return kwargs


ClaimFormSet = inlineformset_factory(
    Product,
    Claim,
    form=ClaimForm,
    formset=BaseProductDerivativeFormSet,
    extra=1,
    can_delete=True
)


class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        fields = ['evidence_type', 'issuer', 'date', 'summary']




EvidenceFormSet = inlineformset_factory(
    Product,
    Evidence,
    form=EvidenceForm,
    extra=1,
    can_delete=True
)

