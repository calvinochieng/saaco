from django import forms
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

# class UniqueEmailValidator(UniqueValidator):
#     def filter_queryset(self, value, queryset):
#         return queryset.filter(email=value)

# class UniqueUsernameValidator(UniqueValidator):
#     def filter_queryset(self, value, queryset):
#         return queryset.filter(username=value)

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea)

