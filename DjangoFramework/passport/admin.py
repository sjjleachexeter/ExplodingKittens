from django.contrib import admin

from passport.models import Product, Ingredient


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


