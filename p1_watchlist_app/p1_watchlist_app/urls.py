from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watchmate/', include('watchmate.urls')),  # Add this line
]
