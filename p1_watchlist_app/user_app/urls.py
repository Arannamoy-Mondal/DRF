from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include
from .views import registeration_view

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),  # Add this line
    path('register', registeration_view, name='register'),  # Add this line
]