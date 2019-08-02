from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
        message="Momo number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Profile(models.Model):
    gender_choices = (
        ("Male", 'M'),
        ("Female", "F"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    momo_name= models.CharField(max_length=50)
    momo_number = models.CharField(max_length=14, validators=[phone_regex,])
    date_of_birth = models.DateField()
    picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    gender = models.CharField(max_length=1, )

    def has_unconfirmed_ref_number(self):
        next_payment_list = Pledge.objects.filter(
            paid=False,
            confirm_received=False,
            profile=self
        )
        if len(next_payment_list)>0:
            return True
        else:
            return False

class ContactMessage(models.Model):
    phone_number = models.CharField(max_length=14, validators=[phone_regex,], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_sent',)

        


class Pledge(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="pledges")
    amount = models.PositiveIntegerField()
    date_pledged = models.DateTimeField(auto_now=True)
    payment_due = models.DateTimeField(blank=True, null=True)
    amount_to_pay = models.PositiveIntegerField(blank=True, null=True)
    reference_number = models.CharField(max_length=20, blank=True)
    confirm_received = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_pledged',)
    
    def __str__(self):
        return f'<Pledge: {self.profile.user.username} | {self.amount} '
    
    def __repr__(self):
        return f'<Pledge: {self.profile.user.username} | {self.amount} '
    

    
