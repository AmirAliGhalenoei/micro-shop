from django.db.models.signals import post_save
from .models import User, Profile


def create_profile(sender, *args, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
post_save.connect(create_profile, User)