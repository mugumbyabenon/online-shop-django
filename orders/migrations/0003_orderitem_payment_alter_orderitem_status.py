# Generated by Django 4.0 on 2023-05-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='payment',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(default='Pending Payment', max_length=30),
        ),
    ]
