from django.db import models

from usuario.models import Usuario

class NaturalPerson(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="person")
    name = models.CharField(max_length=100)
    date_birth = models.DateField()
    document_type = models.CharField(max_length=20, null=True, blank=True)
    document_number = models.CharField(max_length=30, null=True, blank=True)
    document_country = models.CharField(max_length=2, null=True, blank=True)
    note = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"