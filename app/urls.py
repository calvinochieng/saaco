from django.urls import path
from app.views import index, about,contact,terms, policy, home

urlpatterns = [
    path('', index, name = 'index'),
    path('home/', home, name='home'),

    path('about', about, name = 'about'),
    path('contact', contact, name = 'contact'),
    path('terms', terms, name = 'terms'),
    path('policy', policy, name = 'policy'),
]

