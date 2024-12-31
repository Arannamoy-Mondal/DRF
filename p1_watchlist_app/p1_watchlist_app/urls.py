from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('watchmate.urls')),  # Add this line
    path('api-auth/', include('rest_framework.urls')),  # Add this line,
    path('user/', include('user_app.urls')),  # Add this line
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
