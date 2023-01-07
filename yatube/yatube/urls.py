from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    # Все адреса с префиксом auth/ 
    # будут перенаправлены в модуль django.contrib.auth
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),

]
