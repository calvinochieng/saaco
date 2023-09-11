from django.contrib import admin
from saaco.models import Group, Membership, Contribution, Contributor
admin.site.register(Group)
# admin.site.register(Person)
admin.site.register(Membership)
admin.site.register(Contribution)
admin.site.register(Contributor)
