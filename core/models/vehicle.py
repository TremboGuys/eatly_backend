from django.db import models

from usuario.models import Usuario

class Vehicle(models.Model):
    idNaturalPerson = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="vehicle")
    idMark = models.ForeignKey('Mark', on_delete=models.PROTECT, related_name="vehicle")
    idColor = models.ForeignKey('Color', on_delete=models.PROTECT, related_name="vehicle")
    VEHICLE_TYPES = [
    ('car', 'Car'),
    ('motorcycle', 'Motorcycle'),
    ('bicycle', 'Bicycle'),
    ]
    tipe = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    model = models.CharField(max_length=100)
    plate = models.CharField(max_length=7, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.model}"