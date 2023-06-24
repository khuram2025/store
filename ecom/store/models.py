from django.db import models
from django.conf import settings

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='store_cover/')
    profile_image = models.ImageField(upload_to='store_profile/')
    description = models.TextField()
    city = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    whatsapp_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
