# Generated by Django 5.0.1 on 2024-01-31 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='asset_id',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='client_order_id',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.CharField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='replaced_by',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='replaces',
            field=models.CharField(blank=True, null=True),
        ),
    ]
