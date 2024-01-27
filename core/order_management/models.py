from django.db import models


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        )
    client_order_id = models.UUIDField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    submitted_at = models.DateTimeField()
    filled_at = models.DateTimeField(
        null=True,
        blank=True,
        )
    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True
        )
    failed_at = models.DateTimeField(
        null=True,
        blank=True,
        )
    replaced_at = models.DateTimeField(null=True, blank=True)
    replaced_by = models.UUIDField(null=True, blank=True)
    replaces = models.UUIDField(null=True, blank=True)
    asset_id = models.UUIDField()
    symbol = models.CharField(max_length=20)
    asset_class = models.CharField(max_length=20)
    notional = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        )
    qty = models.FloatField()
    filled_qty = models.FloatField()
    filled_avg_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    order_class = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    side = models.CharField(max_length=20)
    time_in_force = models.CharField(max_length=20)
    limit_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    stop_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    status = models.CharField(max_length=20)
    extended_hours = models.BooleanField()
    legs = models.JSONField(null=True, blank=True)
    trail_percent = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    trail_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    hwm = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    commission = models.DecimalField(max_digits=20, decimal_places=4)
    subtag = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    commission_bps = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.id}"
