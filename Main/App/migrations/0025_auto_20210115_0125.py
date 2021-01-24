# Generated by Django 3.1.3 on 2021-01-14 18:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0024_auto_20210115_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotions',
            name='time_update',
        ),
        migrations.AddField(
            model_name='promotions',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]