from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse
from app.services import idshortener
class Group(models.Model):
    """Model definition for Group."""
    name = models.CharField(max_length=100)
    description = models.TextField( null=True, blank=True)
    img = models.ImageField(upload_to='group_icons', null=True, blank=True)
    members = models.ManyToManyField( User, through='Membership')
    
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    pkid = models.CharField(max_length=11, unique=True, null=False, blank = True)

    class Meta:
        ordering = ['-date']
        """Meta definition for Group."""

        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name
    
    def memberscount(self):
        return self.membership_set.count()
    
    def contributioncount(self):
        contributions =  Contribution.objects.filter(group=self).count()
        return contributions

    def save(self,*args, **kwargs):
        try:
            self.pkid = idshortener()
        except: 
           raise ValueError('Could not generate KPID') 
        
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Group."""
        return ('')


class Membership(models.Model):
    """Model definition for Membership."""
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    accepted =  models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    phone =  models.CharField(max_length=13, blank =  True, null =  True)


    # TODO: Define fields here

    class Meta:
        ordering = ['date']
        unique_together = [['user', 'group']]
        """Meta definition for Membership."""

        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f'{self.user.username}, {self.group.name}'
    def save(self,*args, **kwargs):
        try:
            if self.group.members.count() == 0:
                self.admin = True
                self.accepted = True
            else: pass
        except: 
           raise ValueError('ERROR') 
        
        super(Membership, self).save(*args, **kwargs)
    

    def get_absolute_url(self):
        """Return absolute url for Membership."""
        return ('')

class Contribution(models.Model):
    def default_json():
        return {'total': 0, 'contributors': []}

    pkid = models.CharField(max_length=11, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contribution_type = models.CharField(max_length=20, default='Other')
    img = models.ImageField(upload_to='contributions', null= True, blank=True)
    budget = models.DecimalField(decimal_places = 2, max_digits=12,  default=0.00)
    contact = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.BooleanField( default= True)
    collected = models.DecimalField( max_digits=12, decimal_places=2, default=0.00)

    jsondata = models.JSONField(default = default_json, blank = True)#{'Calvin Abunga':2300, 'Mark': 4000, 'Hillary': 20000}

    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now =  True)

    class Meta:
        ordering = ['-time']
        verbose_name = ("Contribution")
        verbose_name_plural = ("Contributions")

    def __str__(self):
        return self.title
    
    
    def contributors(self):
        try: list = len(self.jsondata['contributors'])
        except: list = 0
        return list
    def percentage(self):
        # print (self.collected)
        # print(self.budget)
        percent = 0.00
        try:
            percent = round((self.collected/self.budget)*100, 2)
        except:
            percent = 0.00
            
        return percent

    def save(self,*args, **kwargs):
        if not self.pkid:
            try:
                self.pkid = idshortener()
            except: 
               raise ValueError('Could not generate KPID') 
        # print(self.pkid)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Contribution_detail", kwargs={"pk": self.pk})


class Contributor(models.Model):
    """Model definition for Contributor."""
    name  = models.ForeignKey(User, on_delete=models.CASCADE)
    contributing_to = models.ForeignKey(Contribution,  on_delete=models.CASCADE)
    amount = models.DecimalField( max_digits=10, decimal_places=2, default=0.0)
    paid = models.BooleanField(default=True)

    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now =  True)


    # TODO: Define fields here

    class Meta:
        ordering = ['-time']

        unique_together = [['name', 'contributing_to']]
        """Meta definition for Contributor."""

        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'

    def __str__(self):
        return f'{self.name.username}, {self.contributing_to.title}'

    def save(self,*args, **kwargs):        
        try: 
            # print(self.contributing_to.group)
            group =  self.contributing_to.group
            # from saaco.models import Membership
            membership = Membership.objects.filter(group = group, user = self.name).exists()
            # print(membership)
            if membership: 
                # Data that we need 
                from decimal import Decimal
                contribution = self.contributing_to
                current_total = contribution.collected
                pk = self.name.pk
                name = f'{self.name.first_name} {self.name.last_name}'
                print(self.name.username)
                amount = Decimal(self.amount)
                contributor_data = { "pk":pk, "name":name, "amount": str(amount) }
                total = current_total+amount
                try: 
                    # Do the contribution update and contributor saving
                    # Save contributor'''
                    super(Contributor, self).save(*args, **kwargs)

                    # Prepare the contribution Data
                    contribution.jsondata["total"] = str(total)
                    contribution.jsondata["contributors"].append(contributor_data)
                    jsondata = {
                        "total": contribution.jsondata["total"],
                        "contributors": contribution.jsondata["contributors"]
                    }
                    # Then use the Data to update  the contribution
                    Contribution.objects.filter(pkid = self.contributing_to.pkid).update( collected = total, jsondata = jsondata)

                except Exception as e:  raise  Exception(f"Could not save the item in question, try again, Error: {e}")

            else: raise Exception('Contributor Doesnt Exist')  

        except: raise Exception(f'User {self.name} Doesnt Belong To The Group {group}')         
        # super(Contributor, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):        
    #     try: 
    #         group = self.contributing_to.group
    #         # Check if the user is a member of the group
    #         membership = Membership.objects.filter(group=group, user=self.name).exists()
    #         if membership: 
    #             # If the user is a member, proceed with saving the contribution data
    #             contribution = self.contributing_to
    #             current_total = contribution.collected
    #             pk = self.name.pk
    #             name = f'{self.name.first_name} {self.name.last_name}'
    #             amount = self.amount
    #             contributor_data = {"pk": pk, "name": name, "amount": amount}

    #             # Update contribution data
    #             contribution.jsondata["total"] = current_total + amount
    #             contribution.jsondata["contributors"].append(contributor_data)
    #             contribution.collected = contribution.jsondata["total"]
    #             # Save contribution
    #             contribution.save()

    #             # Save contributor
    #             super(Contributor, self).save(*args, **kwargs)
    #         else:
    #             # If the user is not a member, raise an exception
    #             raise Exception('Contribution Doesnt Exist')  
    #     except Exception as e:
    #         # Catch any exceptions and raise a generic exception
    #         raise Exception("Could not save the item in question. Error: {}".format(str(e)))




        