from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)
    url_image = models.URLField(null=True, blank=True)
    public_id_cloudinary = models.CharField(max_length=40, default="")

    class Meta:
        verbose_name_plural = "Categories"