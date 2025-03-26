from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ed_platform.urls', namespace='ed_platform')),
    path('', include('users.urls', namespace='users')),
]
