# Generated by Django 3.0.8 on 2020-08-13 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0002_auto_20200810_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='sellerPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(help_text='Please Enter With Country Code, For Whatsapp notification make sure You have whatsapp Account', max_length=13)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
