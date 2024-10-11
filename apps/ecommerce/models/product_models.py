from django.db import models
from django_advance_thumbnail.fields import AdvanceThumbnailField

from apps.ecommerce.models.base_models import ECommerceBaseModel
from backend.utils.text_choices import ProductsUnits


class ProductsModel(ECommerceBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(
        max_length=100, choices=ProductsUnits.choices, default=ProductsUnits.OTHER
    )
    stock = models.FloatField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_thumbnail = AdvanceThumbnailField(
        source_field="image", upload_to="products/", blank=True, null=True
    )
    unite_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.pk} - {self.name} - {self.unit} - {self.stock} - {self.unite_price} - {self.updated_at}"
