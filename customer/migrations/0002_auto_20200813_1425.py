# Generated by Django 3.0.8 on 2020-08-13 08:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0003_sellerphone'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RatingDetails',
            new_name='RatingDetail',
        ),
    ]
