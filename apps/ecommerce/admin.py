from django.apps import apps
from django.contrib import admin

from apps.ecommerce.models import ProductsModel

# Register your models here.


for model in apps.get_app_config("ecommerce").models.values():
    if model.__name__ != 'ProductsModel':
        admin.site.register(model)


@admin.register(ProductsModel)
class ProductsModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'unit']
