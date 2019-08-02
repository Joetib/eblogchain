from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.conf import settings
from .models import Pledge

import re


User = get_user_model()


@receiver(post_save, sender=Pledge)
def transaction(sender, instance, **kwargs):
    if not (instance.payment_due and instance.amount_to_pay):
        if instance.confirm_received:
            instance.payment_due = timezone.now() + timezone.timedelta(settings.DAYS_TO_PAYMENT)
            instance.amount_to_pay = instance.amount * settings.INTEREST_RATE
            instance.save()
 
@receiver(pre_save, sender=User)
def verify_user_name(sender, instance, **kwargs):
    if  not re.fullmatch('^\+?1?\d{9,15}$', instance.username):
        raise Exception("Username incorrect: Must contain only numbers and have a length of 10 digitss")