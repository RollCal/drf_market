from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),  # 회원가입
    path('logout/', views.UserLogout.as_view()),  # 로그아웃
    path('login/', views.UserLogin.as_view()),     # 로그인
    path('update/<str:username>/', views.update_user, name='update_user'),  # 본인 정보 수정
    path('change_password/', views.change_password, name='change_password'),  # 패스워드 변경
    path('delete/', views.delete_user, name='delete_user'),     # 회원 탈퇴
]
