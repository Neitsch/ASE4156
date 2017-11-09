"""
Models keeps track of all the persistent data around the user profile
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.plaid_middleware import PlaidAPI


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

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.user_id, self.has_bank_linked)


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
    """
    Contains all the user's bank access data (via plaid)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='userbank'
    )
    item_id = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    institution_name = models.CharField(max_length=1000)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    account_name = models.CharField(max_length=1000)
    income = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure = models.DecimalField(max_digits=15, decimal_places=2)


    def current_balance(self, update=False):
        if update or self.current_balance is None:
            self.current_balance = request.plaid.current_balance()
            self.save()
        return self.current_balance
    
    def account_name(self, update=False):
        if update or self.account_name is None:
            self.account_name = request.plaid.account_name()
            self.save()
        return self.account_name

    def income(self, update=False):
        if update or self.income is None:
            self.income = request.plaid.income()
            self.save()
        return self.income
    
    def expenditure(self, update=False):
        if update or self.expenditure is None:
            self.expenditure = request.plaid.expenditure()
            self.save()
        return self.expenditure

    def __str__(self):
        return "IDs:{}, {}, Institution: {}. ".format(self.institution_name, self.id, self.user_id)

