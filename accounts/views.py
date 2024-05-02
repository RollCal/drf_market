from .serializers import UserSerializer, UserUpdateSerializer, PasswordChangeSerializer, UserDeleteSerializer
from .models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all() # User객체 query셋으로 전달
    serializer_class = UserSerializer  # UserSerializer를 serializer_class로 전달

# 로그인
class UserLogin(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "유저가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "username": user.username}, status=status.HTTP_200_OK)
# 로그아웃
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 로그아웃할 수 있도록 설정
    # 인증된 사용자만 로그아웃할 수 있도록 설정
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        # 로그아웃 전에 사용자가 인증되어 있는지 확인
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            return Response(f"로그아웃 되었습니다. {user}님 안녕히가세요!")
        else:
            return Response("로그아웃 실패: 인증되지 않은 사용자입니다.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request, username):
    user = request.user
    if user.username != username:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserUpdateSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"detail": "기존 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "패스워드가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    serializer = UserDeleteSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['password']):
            return Response({"detail": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"detail": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
