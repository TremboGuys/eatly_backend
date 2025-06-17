from django.db import models

class Mark(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Marks"