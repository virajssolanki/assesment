from rest_framework import serializers
from main.models import Transaction


class CreateTansactionSerializer(serializers.ModelSerializer):
    """
    this serialzer is used to validate payload for buy, sell and split transaction
    """
    class Meta:
        model = Transaction
        fields = [
            "trade_type", "qty", "price", "split_ratio", "date"
        ]

    def validate_qty(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity cannot be zero.")
        return value

    def validate_price(self, value):
        if value == 0:
            raise serializers.ValidationError("Price cannot be zero.")
        return value

    def validate(self, data):
        trade_type = data.get('trade_type', None)
        qty = data.get('qty', None)
        price = data.get('price', None)
        split_ratio = data.get('split_ratio', None)

        errors = {}
        if trade_type == 'SPLIT':
            if split_ratio is None:
                errors['split_ratio'] = "split_ratio is required"
        elif trade_type in ['BUY', 'SELL']:
            if qty is None:
                errors['qty'] = "qty is required"
            if price is None:
                errors['price'] = "price is required"
        
        if errors:
            raise serializers.ValidationError(errors)
            
        return data


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = [
            "trade_type", "qty", "price", "split_ratio", "date", 
            "avg_buy_price", "total_holding_qty", "balance_qty"
        ]


class HoldingViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = [
            "date", "avg_buy_price", "total_holding_qty"
        ]