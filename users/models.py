from django.db import models
from django.conf import settings

class Waiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add any additional fields or methods specific to Waiters

    def __str__(self):
        return self.name

class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add any additional fields or methods specific to Managers

    def __str__(self):
        return self.name

class CEO(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add any additional fields or methods specific to CEO

    def __str__(self):
        return self.name
