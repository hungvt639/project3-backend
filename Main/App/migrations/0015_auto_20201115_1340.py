# Generated by Django 3.1.3 on 2020-11-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='from_saleprice',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='to_saleprice',
            field=models.IntegerField(default=0),
        ),
    ]
