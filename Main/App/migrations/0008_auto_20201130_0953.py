# Generated by Django 3.1.3 on 2020-11-30 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_order_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Chờ xác nhận'), (2, 'Chờ lấy hàng'), (3, 'Đang giao'), (4, 'Đã giao'), (5, 'Đã hủy'), (6, 'Đã xóa')], default=1),
        ),
    ]