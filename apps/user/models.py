from django.contrib.auth.models import AbstractUser
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL

class User(AbstractUser):
    imagen=models.ImageField(upload_to='users/%Y%m%d',null=True,blank=True)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

