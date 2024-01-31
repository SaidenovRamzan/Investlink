# Generated by Django 5.0.1 on 2024-01-31 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('client_order_id', models.UUIDField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('submitted_at', models.DateTimeField()),
                ('filled_at', models.DateTimeField(blank=True, null=True)),
                ('expired_at', models.DateTimeField(blank=True, null=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('failed_at', models.DateTimeField(blank=True, null=True)),
                ('replaced_at', models.DateTimeField(blank=True, null=True)),
                ('replaced_by', models.UUIDField(blank=True, null=True)),
                ('replaces', models.UUIDField(blank=True, null=True)),
                ('asset_id', models.UUIDField()),
                ('symbol', models.CharField(max_length=20)),
                ('asset_class', models.CharField(max_length=20)),
                ('notional', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('qty', models.FloatField()),
                ('filled_qty', models.FloatField()),
                ('filled_avg_price', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('order_class', models.CharField(blank=True, max_length=20)),
                ('order_type', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('side', models.CharField(max_length=20)),
                ('time_in_force', models.CharField(max_length=20)),
                ('limit_price', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('stop_price', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('status', models.CharField(max_length=20)),
                ('extended_hours', models.BooleanField()),
                ('legs', models.JSONField(blank=True, null=True)),
                ('trail_percent', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('trail_price', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('hwm', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('commission', models.CharField(blank=True, max_length=100, null=True)),
                ('subtag', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('commission_bps', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]