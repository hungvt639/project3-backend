# Generated by Django 3.1.3 on 2020-11-15 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0015_auto_20201115_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=1000)),
                ('file', models.FileField(blank=True, upload_to='notifies')),
                ('status', models.IntegerField(choices=[(1, 'Chưa xem'), (2, 'Đã xem')], default=1)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
