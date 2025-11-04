from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Aquí puedes añadir campos futuros (ej. 'institution')
    pass
# Create your models here.
