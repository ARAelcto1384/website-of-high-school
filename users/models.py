from django.db import models
from quiz_app.models import User
from extensions.utils import jalali_converter
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name='پروفایل', blank=True, null=True)
