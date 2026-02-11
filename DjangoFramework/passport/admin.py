from django.contrib import admin

from passport.models import Product, Ingredient, ProductIngredient, Node, Stage, Evidence, Claim, ClaimEvidence


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductIngredient)
class ProductIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass

@admin.register(ClaimEvidence)
class ClaimEvidenceAdmin(admin.ModelAdmin):
    pass