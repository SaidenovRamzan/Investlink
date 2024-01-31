import datetime
from rest_framework import serializers


class DeleteQueryParametersSerializer(serializers.Serializer):
    qty = serializers.CharField(required=False, allow_blank=True, max_length=20)
    percentage = serializers.CharField(required=False, allow_blank=True, max_length=20)

    def validate_qty(self, value):
        if value:
            try:
                float_value = float(value)
            except ValueError:
                raise serializers.ValidationError("qty must be a valid number")
            
            if not 0 <= float_value <= 1000000000:  # Adjust the upper bound as needed
                raise serializers.ValidationError("qty must be between 0 and 1000000000")
            
            if len(value.split('.')[-1]) > 9:
                raise serializers.ValidationError("qty can accept up to 9 decimal points")

        return value

    def validate_percentage(self, value):
        if value:
            try:
                float_value = float(value)
            except ValueError:
                raise serializers.ValidationError("percentage must be a valid number")
            
            if not 0 <= float_value <= 100:
                raise serializers.ValidationError("percentage must be between 0 and 100")

            if len(value.split('.')[-1]) > 9:
                raise serializers.ValidationError("percentage can accept up to 9 decimal points")

        return value


class ListOrdersQueryParametersSerializer(serializers.Serializer):
    status = serializers.CharField(default='open', required=False)
    limit = serializers.IntegerField(default=50, required=False)
    after = serializers.CharField(required=False)
    until = serializers.CharField(required=False)
    direction = serializers.CharField(default='desc', required=False)
    nested = serializers.BooleanField(default=False, required=False)
    symbols = serializers.CharField(required=False)
    qty_above = serializers.FloatField(required=False)
    qty_below = serializers.FloatField(required=False)
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
    