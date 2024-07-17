from django.urls import path
from api.views import api_home, api_groups,api_contributors
urlpatterns = [
    path('', api_home, name = 'api_home'),
    path("groups/", api_groups, name="api_groups"),
    path("C-<pkid>/contributors/", api_contributors, name="api_contributors")
]
