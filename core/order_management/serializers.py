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
        

class TakeProfitSerializer(serializers.Serializer):
    limit_price = serializers.CharField(required=False)


class StopLossSerializer(serializers.Serializer):
    stop_price = serializers.CharField(required=False)
    limit_price = serializers.CharField(required=False)


class OrderCreateSerializer(serializers.Serializer):
    SIDE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('buy_minus', 'buy_minus'),
        ('sell_plus', 'sell_plus'),
        ('sell_short', 'sell_short'),
        ('sell_short_exempt', 'sell_short_exempt'),
        ('undisclosed', 'undisclosed'),
        ('cross', 'cross'),
        ('cross_short', 'cross_short'),
    ]
    Type_CHOICES = [
        ('market', 'market'),
        ('limit', 'limit'),
        ('stop', 'stop'),
        ('stop_limit', 'stop_limit'),
        ('trailing_stop', 'trailing_stop'),
    ]
    Time_In_Force_CHOICES = [
        ('day', 'day'),
        ('gtc', 'gtc'),
        ('opg', 'opg'),
        ('cls', 'cls'),
        ('ioc', 'ioc'),
        ('fok', 'fok'),
    ]
    Extended_Hours_CHOICES = [
        ('', ''),
        ('true', 'true'),
        ('false', 'false'),
    ]
    Order_Class_CHOICES = [
        ('', ''),
        ('simple', 'simple'),
        ('bracket', 'bracket'),
        ('oco', 'oco'),
        ('oto', 'oto'),
    ]
    
    symbol = serializers.CharField(required=True)
    qty = serializers.CharField(required=False, allow_blank=True)
    notional = serializers.CharField(required=False, allow_blank=True)
    side = serializers.ChoiceField(choices=SIDE_CHOICES, required=True)
    type = serializers.ChoiceField(choices=Type_CHOICES, required=True)
    time_in_force = serializers.ChoiceField(choices=Time_In_Force_CHOICES, required=True)
    limit_price = serializers.CharField(required=False, allow_blank=True)
    stop_price = serializers.CharField(required=False, allow_blank=True)
    trail_price = serializers.CharField(required=False, allow_blank=True)
    trail_percent = serializers.CharField(required=False, allow_blank=True)
    extended_hours = serializers.ChoiceField(choices=Extended_Hours_CHOICES, required=True)
    client_order_id = serializers.CharField(max_length=48, required=False, allow_blank=True)
    order_class = serializers.ChoiceField(choices=Order_Class_CHOICES, required=True)
    commission = serializers.CharField(required=False, allow_blank=True)
    commission_bps = serializers.CharField(required=False, allow_blank=True)
    source = serializers.CharField(required=False, allow_blank=True)
    instructions = serializers.CharField(required=False, allow_blank=True)
    subtag = serializers.CharField(required=False, allow_blank=True)
    swap_fee_bps = serializers.CharField(required=False, allow_blank=True)
    take_profit = TakeProfitSerializer(required=False)
    stop_loss = StopLossSerializer(required=False)

    def validate(self, data):
        if data.get('qty'):
            if data.get('notional'):
                raise serializers.ValidationError("Dollar amount to trade. Cannot work with qty. Can only work for market order types and time_in_force = day")
            elif (('.') in data.get('qty')) and ((data.get('type') == 'market') or (data.get('time_in_force') == 'day')):
                raise serializers.ValidationError("Number of shares to trade. Can be fractionable for only market and day order types.")
            
        if data.get('notional'):
            if data.get('qty'):
                raise serializers.ValidationError("Dollar amount to trade. Cannot work with qty")
            elif (data.get('type') != 'market') or (data.get('time_in_force') != 'day'):
                raise serializers.ValidationError("Dollar amount to trade. Cannot work with qty. Can only work for market order types and time_in_force = day")
        
        if data.get('limit_price'):
            if data.get('type') not in ['limit', 'stop_limit']:
                raise serializers.ValidationError("limit_price Required if type is limit or stop_limit")
            
        if data.get('stop_price'): 
            if data.get('type') not in ['stop', 'stop_limit']:
                raise serializers.ValidationError("stop_price Required if type is stop or stop_limit")
        
        if data.get('type') == 'trailing_stop': 
            if not (data.get('trail_price') or data.get('trail_percent')):
                raise serializers.ValidationError("if type is trailing_stop, then one of trail_price or trail_percent is required")
           
        if data.get('extended_hours'):
            if (data.get('type') != 'limit') or (data.get('time_in_force') != 'day'):
                raise serializers.ValidationError("Defaults to false. If true, order will be eligible to execute in premarket/afterhours. Only works with type limit and time_in_force = day.")
            
        if data.get('take_profit'):
            if data.get('type') != 'limit_price':
                raise serializers.ValidationError("Takes in a string/number value for limit_price")
            
        if data.get('stop_loss'):
            if (data.get('type') != 'limit_price') and (data.get('type') != 'stop_price'):
                raise serializers.ValidationError("Takes in a string/number values for stop_price and limit_price")
            
        if data.get('type') == 'market':
            if data.get('stop_price') or data.get('limit_price'):
                raise serializers.ValidationError("market orders require no stop or limit price")
        
        if data.get('type') == 'limit':
            if not data.get('limit_price'):
                raise serializers.ValidationError("limit orders require a limit price")
    
        if not data.get('qty') and  not data.get('notional'):
            raise serializers.ValidationError("qty or notional is required")
                 
        return data

    
        
    

