from django.db import models

from usuario.models import Usuario

class Restaurant(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="restaurant")
    cnpj = models.CharField(max_length=14, null=True, blank=True, verbose_name="CNPJ")
    average_delivery_time = models.SmallIntegerField()
    description = models.CharField(max_length=255)
    note = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.user.first_name}"