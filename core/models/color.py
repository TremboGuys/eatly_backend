from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name