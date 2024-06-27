from django.db import models
from django.contrib.auth.models import User
from applications.ad.models import Ad


class Application(models.Model):
    ad = models.ForeignKey(Ad, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
