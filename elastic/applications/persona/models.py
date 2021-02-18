from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        'email addres',
        unique = True,
        error_messages = {
            'unique': 'Un usuario con ese correo ya existe'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    is_client = models.BooleanField(
        'client',
        default=True


    )

    is_verfied = models. BooleanField(
        'verified',
        null=True,
        default=True

        
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username


