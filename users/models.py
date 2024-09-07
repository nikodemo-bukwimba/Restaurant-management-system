from django.db import models
from django.conf import settings
from django.utils import timezone

class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Waiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name='waiters')

    def __str__(self):
        return self.name

class CEO(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shift(models.Model):
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Shift for {self.waiter.name} - {'Completed' if self.completed else 'Ongoing'}"
