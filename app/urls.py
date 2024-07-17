from django.urls import path
from app.views import index, home, groups, group, contributions, contribution,add, profile, join_group

urlpatterns = [
    path('', index, name = 'index'),
    path('home/', home, name='home'),
    path('groups/', groups, name = 'groups'),
    path("G-<pkid>", group, name="group"),
    path("contributions/", contributions, name = "contributions"),
    path("C-<pkid>", contribution, name="contribution"),
    path("join/group/<pkid>", join_group, name = "join_group"),

    path('add/', add, name = 'add'),
    path("profile/", profile, name="profile"),
]

