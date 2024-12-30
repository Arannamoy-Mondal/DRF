from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('watchmate.urls')),  # Add this line
    path('api-auth/', include('rest_framework.urls')),  # Add this line
]
