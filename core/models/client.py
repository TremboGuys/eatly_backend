from django.db import models

from usuario.models import Usuario

class Client(models.Model):
    class Genre(models.IntegerChoices):
        MASCULINE = 1, "Masculine",
        FEMININE = 2, "Feminine",
        HIDDEN = 3, "Hidden"
    user = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="client")
    genre = models.IntegerField(choices=Genre, null=True)
    date_birth = models.DateField()
    cpf = models.CharField(max_length=11, null=True, verbose_name="CPF")

    def __str__(self):
        return f"{self.user.email}"