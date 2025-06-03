from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    neighborhood = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    complement = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=8)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name_plural = "Addresses"