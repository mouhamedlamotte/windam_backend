from django.db import models
from django.contrib.auth.models import AbstractUser
import shortuuid

# Create your models here.


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False, null=False)
    username = models.CharField(max_length=255, unique=True, default=shortuuid.uuid)
    email = models.EmailField(max_length=255, unique=True, blank=False)