from django.db import models
from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse as api_reverse

User = get_user_model()

# Create your models here.

class BlogPost(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    content     = models.CharField(max_length=200)
    title       = models.CharField(max_length=200)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-postings:post-rud", kwargs={'id':self.id}, request=request)   
