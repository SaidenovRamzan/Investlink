from rest_framework import serializers
from .models import Order
import datetime


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ListOrdersQueryParametersSerializer(serializers.Serializer):
    status = serializers.CharField(default='open', required=False)
    limit = serializers.IntegerField(default=50, required=False)
    after = serializers.CharField(default='2000-03-16T18:38:01.942282Z', required=False)
    until = serializers.CharField(default='2060-03-16T18:38:01.942282Z', required=False)
    direction = serializers.CharField(default='desc', required=False)
    nested = serializers.BooleanField(default=False, required=False)
    symbols = serializers.CharField(default='AAPL,TSLA,MSFT', required=False)
    qty_above = serializers.IntegerField(default=None, required=False)
    qty_below = serializers.IntegerField(default=None, required=False)
    subtag = serializers.CharField(allow_blank=True, required=False)

    def validate_status(self, value):
        if value in ['all', 'open', 'closed']:
            return value
        else: serializers.ValidationError
        
    def validate_direction(self, value):
        if value in ['asc', 'desc']:
            return value
        else: serializers.ValidationError
        
    def validate_after(self, value):
        try:
            datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S.%fZ')
            return value
        except ValueError:
            return serializers.ValidationError
        
    def validate_until(self, value):
        try:
            datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S.%fZ')
            return value
        except ValueError:
            return serializers.ValidationError
        
    def validate_nested(self, value):
        if value in [True, False]:
            return value
        else: serializers.ValidationError
    
        
    

