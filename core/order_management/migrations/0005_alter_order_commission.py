# Generated by Django 5.0.1 on 2024-01-27 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0004_order_commission_bps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='commission',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]