"""
URL configuration for the_sheland project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rooms/', include('rooms.urls')),
    path('api/game/', include('game.urls')),
    path('api/users/', include('users.urls')),
]
