from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, 
    Wallet, 
    Transaction
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Wallet.objects.create(user=user)
        return user

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(source='get_transaction_type_display')
    
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount']