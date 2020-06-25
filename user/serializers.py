from rest_framework import serializers
from .models import Users
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Users
        fields = ('bio', 'user_id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username','first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user