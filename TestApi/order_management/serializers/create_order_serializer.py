from enum import Enum
from rest_framework import serializers


class SideChoices(Enum):
    BUY = 'buy'
    SELL = 'sell'
    BUY_MINUS = 'buy_minus'
    SELL_PLUS = 'sell_plus'
    SELL_SHORT = 'sell_short'
    SELL_SHORT_EXEMPT = 'sell_short_exempt'
    UNDISCLOSED = 'undisclosed'
    CROSS = 'cross'
    CROSS_SHORT = 'cross_short'


class TypeChoices(Enum):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop_limit'
    TRAILING_STOP = 'trailing_stop'


class TimeInForceChoices(Enum):
    DAY = 'day'
    GTC = 'gtc'
    OPG = 'opg'
    CLS = 'cls'
    IOC = 'ioc'
    FOK = 'fok'


class ExtendedHoursChoices(Enum):
    DEFAULT = ''
    FALSE = 'false'
    TRUE = 'true'


class OrderClassChoices(Enum):
    DEFAULT = ''
    SIMPLE = 'simple'
    BRACKET = 'bracket'
    OCO = 'oco'
    OTO = 'oto'


class TakeProfitSerializer(serializers.Serializer):
    limit_price = serializers.CharField(required=False)


class StopLossSerializer(serializers.Serializer):
    stop_price = serializers.CharField(required=False)
    limit_price = serializers.CharField(required=False)
    
    
class OrderCreateSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=True)
    qty = serializers.CharField(required=False, allow_blank=True)
    notional = serializers.CharField(required=False, allow_blank=True)
    side = serializers.ChoiceField(choices=[(item.value, item.value) for item in SideChoices], required=True)
    type = serializers.ChoiceField(choices=[(item.value, item.value) for item in TypeChoices], required=True)
    time_in_force = serializers.ChoiceField(choices=[(item.value, item.value) for item in TimeInForceChoices], required=True)
    limit_price = serializers.CharField(required=False, allow_blank=True)
    stop_price = serializers.CharField(required=False, allow_blank=True)
    trail_price = serializers.CharField(required=False, allow_blank=True)
    trail_percent = serializers.CharField(required=False, allow_blank=True)
    extended_hours = serializers.ChoiceField(choices=[(item.value, item.value) for item in ExtendedHoursChoices])
    client_order_id = serializers.CharField(max_length=48, required=False, allow_blank=True)
    order_class = serializers.ChoiceField(choices=[(item.value, item.value) for item in OrderClassChoices], required=True)
    commission = serializers.CharField(required=False, allow_blank=True)
    commission_bps = serializers.CharField(required=False, allow_blank=True)
    source = serializers.CharField(required=False, allow_blank=True)
    instructions = serializers.CharField(required=False, allow_blank=True)
    subtag = serializers.CharField(required=False, allow_blank=True)
    swap_fee_bps = serializers.CharField(required=False, allow_blank=True)
    take_profit = TakeProfitSerializer(required=False)
    stop_loss = StopLossSerializer(required=False)

    def validate_qty(self, value):
        qty = value
        notional = self.initial_data.get('notional', '')
        side = self.initial_data.get('side', '')
        time_in_force = self.initial_data.get('time_in_force', '')

        if notional:
            raise serializers.ValidationError("Dollar amount to trade. Cannot work with qty. Can only work for market order types and time_in_force = day")
        
        elif ('.' in qty) and  not((side == 'market') and (time_in_force == 'day')):
            raise serializers.ValidationError("Qty must be a valid integer.")
            
        elif not (qty or notional):
            raise serializers.ValidationError("qty or notional is required")

        return value

    def validate_notional(self, value):
        notional = value
        qty = self.initial_data.get('qty', '')
        side = self.initial_data.get('side', '')
        time_in_force = self.initial_data.get('time_in_force', '')
        
        if qty and notional:
            raise serializers.ValidationError("Notional cannot be provided without Qty or Side.")
        
        elif (time_in_force == 'day') and (side == 'market'):
            raise serializers.ValidationError("Notional must not be provided when Qty is provided.")
        
        return value
    
    def validate_type(self, value):
        type_order = value 
        limit_price = self.initial_data.get('limit_price', '')
        stop_price = self.initial_data.get('stop_price', '')
        trail_price = self.initial_data.get('trail_price', '')
        trail_percent = self.initial_data.get('trail_percent', '')
        
        if (limit_price or stop_price) and (type_order == 'market'):
            raise serializers.ValidationError("market orders require no stop or limit price")
        
        elif trail_price != '' and (type_order == 'market'):
            raise serializers.ValidationError("market orders must not have trail_price")
        
        elif trail_percent != '' and (type_order == 'market'):
            raise serializers.ValidationError("market orders must not have trail_percent")
        
        elif (type_order == 'stop') and (limit_price or trail_percent or trail_price):
            
            if limit_price:
                raise serializers.ValidationError("stop orders require no limit price")
            
            elif trail_price:
                raise serializers.ValidationError("stop orders require no trail price")
            
            elif trail_percent:
                raise serializers.ValidationError("stop orders require no trail percent")
        
        return value

    def validate_limit_price(self, value):
        limit_price = value
        order_type = self.initial_data.get('type', '')

        if order_type in ['limit', 'stop_limit'] and not limit_price:
            raise serializers.ValidationError("Limit price is required for order types 'limit' or 'stop_limit'.")

        return value

    def validate_stop_price(self, value):
        stop_price = value
        order_type = self.initial_data.get('type', '')

        if order_type in ['stop', 'stop_limit'] and not stop_price:
            raise serializers.ValidationError("Stop price is required for order types 'stop' or 'stop_limit'.")

        return value
    