from django.db import models

class Telephone(models.Model):
    class TypeTelephone(models.IntegerChoices):
        CELLPHONE = 1, "Cellphone"
        LANDLINE = 2, "Landline"
    telephone_type = models.IntegerField(choices=TypeTelephone)
    number_e164 = models.CharField(max_length=15)
    is_principal = models.BooleanField()

    def __str__(self):
        return f"{self.number_e164[0:3]} {self.number_e164[3:]}"