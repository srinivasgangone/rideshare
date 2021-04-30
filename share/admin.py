from django.contrib import admin

# Register your models here.
from .models import User, Ride

admin.site.register(User)
admin.site.register(Ride)