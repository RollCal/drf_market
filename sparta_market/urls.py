from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # accounts 앱의 엔드포인트를 /api/accounts/로 변경
    path('api/products/', include('products.urls')),
    # path('api/products/', include('products.urls')),  # products 앱의 엔드포인트를 /api/products/로 변경
]

