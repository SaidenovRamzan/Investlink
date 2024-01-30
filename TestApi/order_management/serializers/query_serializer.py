import datetime
from rest_framework import serializers


class ListOrdersQueryParametersSerializer(serializers.Serializer):
    status = serializers.CharField(default='open', required=False)
    limit = serializers.IntegerField(default=50, required=False)
    after = serializers.CharField(default='2000-03-16T18:38:01.942282Z', required=False)
    until = serializers.CharField(default='2060-03-16T18:38:01.942282Z', required=False)
    direction = serializers.CharField(default='desc', required=False)
    nested = serializers.BooleanField(default=False, required=False)
    symbols = serializers.CharField(default='AAPL,TSLA,MSFT', required=False)
    qty_above = serializers.CharField(default='-1', required=False)
    qty_below = serializers.CharField(default='10000000000', required=False)
    subtag = serializers.CharField(allow_blank=True, required=False)

    def validate_status(self, value):
        if value in ['all', 'open', 'closed']:
            return value
        raise serializers.ValidationError("Invalid status value")
        
    def validate_direction(self, value):
        if value in ['asc', 'desc']:
            return value
        raise serializers.ValidationError("Invalid direction value")
        
    def validate_after(self, value):
        try:
            time = datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S.%fZ')
            return time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        except ValueError as e:
            raise serializers.ValidationError(f"Invalid after value {e}")
        
    def validate_until(self, value):
        try:
            time = datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S.%fZ')
            return time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        except ValueError as e:
            raise  serializers.ValidationError(f"Invalid until value {e}")
        
    def validate_nested(self, value):
        if value in [True, False]:
            return value
        raise serializers.ValidationError("Invalid nested value")
    