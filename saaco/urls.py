from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from app.views import error_404,error_500, register

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path("user/register/", register, name="register"),
    path("user/", include('django.contrib.auth.urls')), 
]

handler404 = error_404
handler500 = error_500
