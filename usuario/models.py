from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Usuario(AbstractUser):
    username = None
    email = models.EmailField(_("e-mail address"), unique=True)
    photo = models.URLField(null=False, blank=True)
    public_id_cloudinary = models.CharField(max_length=40, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-date_joined"]

class EmailVerificationUser(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    date_time = models.DateTimeField(auto_now_add=True)