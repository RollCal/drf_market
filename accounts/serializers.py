from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data): #validated_data를 기입하여 유효성이 확인된 값을 기반으로 User객체 생성
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            name = validated_data['name'],
            password = validated_data['password'],
        )
        return user
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'nickname']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField()
