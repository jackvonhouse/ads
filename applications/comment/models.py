from django.db import models
from django.contrib.auth.models import User
from applications.ad.models import Ad


class Comment(models.Model):
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
