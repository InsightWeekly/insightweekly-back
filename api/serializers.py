from rest_framework import serializers
from .models import Account, News

class AccountSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password_check', 'interest_category']
        extra_kwargs = {
            'password': {'write_only': True},
            'interest_category': {'read_only': True}
            }

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # We don't set interest_category at signup anymore
        return user

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__' 