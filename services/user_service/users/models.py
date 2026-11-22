from django.db import models
from django_jalali.db import models as jmodels
from django.core.validators import validate_integer
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from .validators import validate_phone


class User(AbstractUser):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_integer, validate_phone]
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    email = None
    username = None
    first_name = None
    last_name = None

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(max_length=80, unique=True, null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    date_of_birth = jmodels.jDateField(null=True, blank=True)
    
    verified_email = models.BooleanField(default=False)

    # django-jalali
    objects = jmodels.jManager()

    def __str__(self):
        return f"{self.user.phone}"



