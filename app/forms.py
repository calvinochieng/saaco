from django import forms
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Group, Membership, Contribution, Contributor

# class UniqueEmailValidator(UniqueValidator):
#     def filter_queryset(self, value, queryset):
#         return queryset.filter(email=value)

# class UniqueUsernameValidator(UniqueValidator):
#     def filter_queryset(self, value, queryset):
#         return queryset.filter(username=value)

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name =forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class GroupForm(forms.ModelForm):
    item = forms.CharField(required=True, widget= forms.HiddenInput(attrs = {'value': 'group'}))
    name =  forms.CharField(required = True, widget=forms.TextInput(attrs={ 'class': 'input is-medium ', 'placeholder':'Group Name'}))

    class Meta:
        model = Group
        fields = ("name",)

class ContributionForm(forms.ModelForm):   
    EDUCATION = 'Education'
    BUSINESS = 'Business'
    CHAMA = 'Chama'
    MEDICAL = 'Medical'
    RELIGIOUS = 'Religious'
    WEDDING = 'Wedding'
    FUNERAL = 'Funeral'
    OTHER = 'Other'

    CONTRIBUTION_TYPE_CHOICES = [
        (EDUCATION, 'Education'),
        (BUSINESS, 'Business'),
        (CHAMA, 'Chama'),
        (MEDICAL, 'Medical'),
        (RELIGIOUS, 'Religious'),
        (WEDDING, 'Wedding'),
        (FUNERAL, 'Funeral'),
        (OTHER, 'Other'),
    ]
    item = forms.CharField(required= True,widget=forms.HiddenInput(attrs = {'value': 'contribution'}))
    title =  forms.CharField(required = True, widget=forms.TextInput(attrs={ 'class': 'is-normal input', 'placeholder':'Title Of Your Contribution'}))
    description = forms.CharField(required=True, widget =forms.Textarea(attrs={
        'class': 'textarea ',
        'rows' : '2',
        'placeholder':'Write a Good Summary About your Contribution'})
    )
    contribution_type = forms.ChoiceField(
        choices=CONTRIBUTION_TYPE_CHOICES,
        required=True
    )
    # group = forms.ChoiceField( required=True)
    
    class Meta:
        model = Contribution
        fields = ("title","description",'contribution_type','group', "budget", )


class ContributorForm(forms.Form):
    pk = forms.CharField(required=False,widget=forms.HiddenInput())
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={ 'class': 'is-medium input', 'placeholder':'Contributor\'s Name'}))
    amount = forms.CharField(required = True, widget=forms.NumberInput(attrs={ 'class': 'is-medium input', 'placeholder':'Amount'}) )



