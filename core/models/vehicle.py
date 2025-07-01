from django.db import models

from core.models import NaturalPerson

class Vehicle(models.Model):
    idNaturalPerson = models.ForeignKey(NaturalPerson, on_delete=models.PROTECT, related_name="vehicles")
    idMark = models.ForeignKey('Mark', on_delete=models.PROTECT, related_name="vehicles")
    idColor = models.ForeignKey('Color', on_delete=models.PROTECT, related_name="vehicles")
    VEHICLE_TYPES = [
    ('car', 'Car'),
    ('motorcycle', 'Motorcycle'),
    ('bicycle', 'Bicycle'),
    ]
    type_vehicle = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    model = models.CharField(max_length=100)
    plate = models.CharField(max_length=8, unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_validate = models.BooleanField(default=False)
    url_crlv = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.model}"