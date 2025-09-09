from django.db import models

from usuario.models import Usuario

class Address(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="addresses")
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    complement = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=8)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"