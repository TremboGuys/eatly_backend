from django.db import models

from usuario.models import Usuario

class Client(models.Model):

    user = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="restaurant")
    date_birth = models.DateField()
    cnpj = models.CharField(max_length=11, null=True, verbose_name="CNPJ")

    def __str__(self):
        return f"{self.user.email}"