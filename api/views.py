from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from app.models import Group, Membership, Contribution, Contributor
from app.forms import RegistrationForm, GroupForm, ContributionForm, ContributorForm

def api_home(request):
    return redirect('home')

def api_groups(request):
    user = request.user
    data = {}
    if not user.is_authenticated: return JsonResponse({'data':'please login'})
    if request.method == 'GET': 
        items = list(Group.objects.filter(members = user).values('name','pkid'))

        data = {'items': items}
        return JsonResponse(data)
    # Craete group from post
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                group = Group.objects.create(name = name)
                # print(group.id)
            except: return JsonResponse(data={'error': 'Error occured while creating group, try again'})
                
            member = Membership.objects.create(
                group = group, user = user
            )
            if form.cleaned_data.get('item') == 'flash':    
                data = {'name': group.name, 'id': group.id}
                return JsonResponse(data)
        group = group.values('pkid','name','description', 'contributioncount', 'memberscount')
        data = {'item': list(group)}
        return JsonResponse(data)
    
def api_contributors(request, pkid=None):
    user = request.user
    if not user.is_authenticated: return JsonResponse({'data':'please login'})
    contributing_to = Contribution.objects.get(pkid = pkid)
    data = {}
    is_admin = True

    # PREVENT PERSONS NOT MEMBERS AND NOT ADMIN
    try:
        is_admin =  Membership.objects.filter(group = contributing_to.group, user = user, accepted = True, admin = True).exists()
    except: pass

    member = Membership.objects.filter()
    if request.method == 'GET': 
        items = list(Contributor.objects.filter(contributing_to = contributing_to).values('pk','name','amount'))

        data = {'items': items}
        return JsonResponse(data)
    # Add contributor from post
    if request.method == "POST" and is_admin:
        form = ContributorForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            name = form.cleaned_data.get('name')
            amount = form.cleaned_data.get('amount')
            if pk:
                try:
                    name = User.objects.get(pk=pk)
                    contributor = Contributor.objects.create(name = name, amount = amount, contributing_to = contributing_to)        
                    contributor = contributor.values('pk','name','amount')
                    data = {'item': list(contributor)}
                    return JsonResponse(data) 
                    
                except: return JsonResponse(data={'error': 'Error occured while adding a contributor, try again'})
            else:
                from decimal import Decimal
                contribution = contributing_to
                current_total = contribution.collected
                # print(contribution.jsondata["total"] )
                pk = ''
                name = name
                amount = Decimal(amount)
                contributor_data = { "pk":pk, "name":name, "amount": str(amount) }
                total = current_total+amount
                # Do the contribution update and contributor saving
                try:
                    # Do the contribution update and contributor saving
                    contribution.jsondata["total"] = str(total)
                    contribution.jsondata["contributors"].append(contributor_data)
                    
                    # print(f'total {total}, Contributors{contribution.jsondata["contributors"]}')
                    # Then update contribtuion
                    jsondata = {
                        "total": contribution.jsondata["total"],
                        "contributors": contribution.jsondata["contributors"]
                    }
                    contributors_num = contribution.contributors()
                    # print(contributors_num)
                    Contribution.objects.filter(pkid=pkid).update( collected = total, jsondata = jsondata)
                    #  Get current number of contributors

                    # contribution.save()
                    print(round((total/contributing_to.budget)*100, 2))

                    data = {"total": contribution.jsondata["total"],'contributors': contributors_num,
                        'name': name, 'amount': amount, 'percentage': f'{round((total/contributing_to.budget)*100, 2)}%'}
                    return JsonResponse(data) 
                
                except Exception as e:  raise  Exception(f"Could not save the item in question, try again, Error: {e}")

        else: return JsonResponse(data={'error':'Invalid form, try again'})

    elif not is_admin:
        print(is_admin)
        data = {'error': "You're not admin on this contribution"}
        return JsonResponse(data) 


