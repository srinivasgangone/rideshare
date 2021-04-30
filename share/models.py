from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils import timezone

from django.conf import settings

from djongo import models

import random
import string


def generate_recovery_code():
    recover_code = ''.join(random.choices(
        string.ascii_letters + string.digits, k=10))
    return recover_code

class TimeModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract=True 


class User(AbstractUser):
    _id = models.ObjectIdField(primary_key=True)
    id = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate_recovery_code()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Ride(TimeModel):
    _id = models.ObjectIdField(primary_key=True)
    id = models.CharField(max_length=200)
    driver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='driver')
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer', blank=True, null=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    cost = models.FloatField()

    class Meta:
        db_table = 'rides'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate_recovery_code()
        super(Ride, self).save(*args, **kwargs)

    def __str__(self):
        return str(self._id)
        