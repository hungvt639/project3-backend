# Generated by Django 3.1.3 on 2021-01-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0023_promotionproducts_promotions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotions',
            name='commant',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]