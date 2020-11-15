# Generated by Django 3.1.3 on 2020-11-15 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_order_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Đặt hàng'), (2, 'Chốt đơn'), (3, 'Đang giao'), (4, 'Đã nhận'), (5, 'Đã hủy'), (6, 'Đã xóa')], default=1),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='App.order'),
        ),
    ]