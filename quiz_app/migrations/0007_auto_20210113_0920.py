# Generated by Django 3.1.1 on 2021-01-13 05:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0006_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='likes',
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='تعداد لایک ها'),
        ),
        migrations.DeleteModel(
            name='likes',
        ),
    ]
