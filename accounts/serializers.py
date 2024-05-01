from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password # Django기본 pw검증모델
from django.contrib.auth import authenticate # 쟝고의 기본 authenticate함수, 선택한 DefaultAuthBackend인 TokenAuth 방식으로 유저 인증

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator #이메일 중복 방지 검증
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일 중복검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호 검증
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data): # password와 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match.'})

        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메서드를 오버라이딩하여, 유저를 생성하고 토큰도 생성가능
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # write_only=True 옵션을 통해 클라이언트 -> 서버의 역직렬화는 가능, 서버 -> 클라이언트 방향의 직렬화는 불가능하도록

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 해당 유저의 토큰을 불러옴
            return token
        raise serializers.ValidationError( # 유저가 가입상태가 아닐 때
            {"error": "Unable to log in with provided credentials."}
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "birth_date", "gender", "introduction")
