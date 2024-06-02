from django.db import models

# Create your models here.

class PosterDetail(models.Model):
    first = models.CharField(max_length=400)
    last = models.CharField(max_length=400,blank=True)
    img = models.ImageField(upload_to="pfps")

    def __str__(self):
        return self.first