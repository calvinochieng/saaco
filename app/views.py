from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from app.models import Group, Membership, Contribution, Contributor
from app.forms import RegistrationForm, GroupForm, ContributionForm, ContributorForm

def index(request):     
    if request.user.is_authenticated: return redirect('home')   
    messages.success(request, 'Welcome, thank you so much for coming by please login / register below')             
    return render(request,'index.html') 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            # user = User.objects.create(email=email, username= username,  first_name =  first_name, last_name = last_name ,password= password )
            try:
                user = User.objects.create_user(email=email, username= username, password= password )
            except:
                messages.error(request,"Username allready exists, try another one")
                return render(request, 'registration/register.html', locals())

            user = authenticate(username=username, password=password)
            update_user = User.objects.filter(username = username).update(first_name =  first_name, last_name = last_name) 

            login(request, user)
            messages.success(request,"Welcome, thank you for signing up")
            return redirect('home')
        else: messages.warning(request,"Some fields were incorrect, check and try again")
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', locals())
  
@login_required( login_url='/user/login/')
def home(request):
    user = request.user
    group_items = Group.objects.filter(members = user)
    items = []
    items = [item for group in group_items for item in group.contribution_set.all() if group.contribution_set.exists()]

    context = {'items': items}
    return render(request, 'home.html', context)

@login_required( login_url='/user/login/')   
def groups(request):
    form = GroupForm()
    user = request.user
    items = Group.objects.filter(members = user)
    context = {'items': items}
    # Craete group from post
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                group = Group.objects.create(name = name)
                messages.success(request,"Your group was created successfully")
                # print(group.id)
            except:
                messages.error(request,"Couldn't create group, try again")
                # print('Cant create group')
            member = Membership.objects.create(
                group = group, user = user
            )
            if form.cleaned_data.get('item') == 'flash': return redirect('/add/?item=contribution')
        return redirect('group', pkid = group.pkid)
    
    return render(request, 'groups.html', context)

@login_required( login_url='/user/login/') 
def group(request, pkid=None):
    item = get_object_or_404(Group, pkid= pkid)
    user =  request.user
    items = Contribution.objects.filter(group=item)
    members = Membership.objects.filter(group = item)

    is_member = None
    try: is_member = Membership.objects.filter(group = item, user = user).exists()
    except: is_member = None

    context = {'item' : item, 'items': items, 'members' : members, 'is_member' : is_member}
    return render(request, 'group.html', context)

@login_required(login_url='/user/login/')
def join_group(request ,pkid = None):
    item = get_object_or_404(Group, pkid= pkid)
    user =  request.user
    try:
        membership =  Membership.objects.create( group = item, user = user )
    except Exception as e:
        messages.warning(request,f"You can't join '{item.name}'. Error: occured")
         
    
    return redirect('group', pkid= pkid)


@login_required( login_url='/user/login/') 
def contributions(request):
    user = request.user
    group_items = Group.objects.filter(members = user)
    items = []

    if request.method == 'GET':
        contribution_type = request.GET.get('type', None)
        if contribution_type: items = [item for group in group_items for item in group.contribution_set.filter(contribution_type = contribution_type) if group.contribution_set.exists()]
        else: items = [item for group in group_items for item in group.contribution_set.all() if group.contribution_set.exists()]

    context = {'items': items}

    form = ContributionForm()
    if request.method == "POST":
        form = ContributionForm(request.POST)
        # print(form)
        if form.is_valid():
            try:
                title =form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                contribution_type = form.cleaned_data.get('contribution_type')
                print(contribution_type)
                budget = form.cleaned_data.get('budget')
                group = form.cleaned_data.get('group')
                contribution = Contribution.objects.create(
                    title = title, description = description, contribution_type = contribution_type,
                    budget = budget, group = group
                    )
                # print(contribution.id)
                messages.success(request,"Contribution was created successfully, start adding contributors and share")
                return redirect('contribution', pkid= contribution.pkid)
            except:
                # If it can not be saved then just redirect back to the add page with contribution as query
                messages.warning(request,"Couldn't create contribution , please try again")
                return redirect('/add/?item=contribution')  

        else:
            print("Not Working")
            messages.warning(request,"Some fields may be inaccurate, please try again") 
            return redirect('/add/?item=contribution')  

    return render(request, 'contributions.html', context)

@login_required( login_url='/user/login/') 
def contribution(request, pkid=None):
    user = request.user
    is_admin = False
    is_member =  False
    
    item = get_object_or_404(Contribution, pkid= pkid)
    group = item.group
    
    # Prevent None Members From Viewing The Contributiuon
    try:
        is_member =  Membership.objects.filter(group = group, user = user).exists()
    except: pass

    # PREVENT PERSONS NOT MEMBERS AND NOT ADMIN From editing the contributions
    try:
        is_admin =  Membership.objects.filter(group = group, user = user, accepted = True, admin = True).exists()
        # print(is_admin)
        form = ContributorForm()
    except: is_admin = False

    return render(request, 'contribution.html', locals())

@login_required( login_url='/user/login/') 
def add(request):
    user = request.user
    if request.method == 'GET':
        item = request.GET.get('item', None)   
        if item == 'group':
            item = 'Group'
            url = '/groups/'
            form  = GroupForm()
            # print(item)

        elif item == 'contribution':
            item = 'Contribution'
            url = '/contributions/'
            form = ContributionForm()
            admin = Membership.objects.filter(user =  user, admin = True, accepted = True).order_by('-date')
            # admin = None


        elif not item: pass #When Item is not provide
        else: item = None #When item is provided but its not a group or contribution
    return render(request, 'app/add.html', locals())

@login_required( login_url='/user/login/')
def profile(request):
    return render(request, 'user/profile.html')


def offline(request):
    return render(request, 'pwa/offline.html')

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

