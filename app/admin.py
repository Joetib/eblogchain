from django.contrib import admin
from .models import Profile, ContactMessage, Pledge

# Register your models here.
admin.site.register(Profile)
admin.site.register(ContactMessage)
admin.site.register(Pledge)