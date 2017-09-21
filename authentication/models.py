"""
Models keeps track of all the persistent data around the user profile
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile represents additional values for a user account
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    has_bank_linked = models.NullBooleanField(
        blank=True, default=False, null=True)


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **_):
    """
    Creates a linked profile when a user account is created
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, **_):
    """
    To be safe, whenever the user profile is saved, we also save the profile
    """
    instance.profile.save()


class UserBank(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_id = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
