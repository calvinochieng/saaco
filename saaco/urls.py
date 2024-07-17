from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from app.views import error_404,error_500, register, offline,about,terms, policy,contact
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('app.urls')),
    #ALL AUTH
    path('accounts/', include('allauth.urls')),
    
    # LOCAL URLS
    path("api/", include('api.urls')),
    path('admin/', admin.site.urls),
    path("user/register/", register, name="register"),
    path("user/", include('django.contrib.auth.urls')), 
    # PWA

    path('sw.js', (TemplateView.as_view(template_name="pwa/sw.js", 
          content_type='application/javascript', )), name='sw.js'),
    path("offline/", offline, name="offline")
]+[

    path('about', about, name = 'about'),
    path('contact', contact, name = 'contact'),
    path('terms', terms, name = 'terms'),
    path('policy', policy, name = 'policy'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error_404
handler500 = error_500
