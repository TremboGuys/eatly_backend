from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)
    url_image = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"