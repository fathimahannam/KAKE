# Generated by Django 4.2.5 on 2023-11-28 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baker', '0010_alter_order_baker_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending', max_length=20),
        ),
    ]
