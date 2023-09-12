from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from app.models import Group, Membership
from app.forms import RegistrationForm

def index(request):                 
    return render(request,'index.html') 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(email=email, username= username, password= password )
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', locals())
  
@login_required( login_url='/user/login/')
def home(request):
    items = Group.objects.all()
    context = {'items': items}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def terms(request):
    return render(request, 'terms.html')
def policy(request):
    return render(request, 'policy.html')

def error_404(request, exception):
    return render(request,'error.html')
def error_500(request):
    return render(request,'error.html')

