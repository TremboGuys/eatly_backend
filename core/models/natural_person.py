from django.db import models

from usuario.models import Usuario

class NaturalPerson(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="person")
    name = models.CharField(max_length=100)
    date_birth = models.DateField()
    cpf = models.CharField(max_length=11, null=True, verbose_name="CPF")

    def __str__(self):
        return f"{self.user.email}"