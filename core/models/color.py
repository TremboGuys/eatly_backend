from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        verbose_name_plural = "Colors"