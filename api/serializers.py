from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    lastname = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)


class StockPriceSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    open = serializers.FloatField()
    lower = serializers.FloatField()
    higher = serializers.FloatField()
    close_variation = serializers.FloatField()

