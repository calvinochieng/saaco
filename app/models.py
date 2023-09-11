from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse
from app.services import idshortener
class Group(models.Model):
    """Model definition for Group."""
    name = models.CharField(max_length=100)
    description = models.TextField( null=True, blank=True)
    img = models.ImageField(upload_to='group_icons/', null=True, blank=True)
    members = models.ManyToManyField( User, through='Membership')
    
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    pkid = models.CharField(max_length=11, unique=True, null=False, blank = True)

    class Meta:
        """Meta definition for Group."""

        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name

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
    phone =  models.CharField(max_length=13)


    # TODO: Define fields here

    class Meta:
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
            else: pass
        except: 
           raise ValueError('ERROR') 
        
        super(Membership, self).save(*args, **kwargs)
    

    def get_absolute_url(self):
        """Return absolute url for Membership."""
        return ('')

class Contribution(models.Model):
    pkid = models.CharField(max_length=11, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='contributions/', null= True, blank=True)
    amount = models.DecimalField(decimal_places = 2, max_digits=8,  default=0.00)
    contact = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.BooleanField( default= True)
    total =models.DecimalField( max_digits=8, decimal_places=2)

    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now =  True)

    class Meta:
        verbose_name = ("Contribution")
        verbose_name_plural = ("Contributions")

    def __str__(self):
        return self.name
    

    def save(self,*args, **kwargs):
        try:
            self.pkid = idshortener()
        except: 
           raise ValueError('Could not generate KPID') 
        
        super(Contribution, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Contribution_detail", kwargs={"pk": self.pk})


class Contributor(models.Model):
    """Model definition for Contributor."""
    name  = models.ForeignKey(User, on_delete=models.CASCADE)
    contributing_to = models.ForeignKey(Contribution,  on_delete=models.CASCADE)
    amount = models.DecimalField( max_digits=7, decimal_places=2, default=0.0)
    paid = models.BooleanField(default=False)


    # TODO: Define fields here

    class Meta:

        unique_together = [['name', 'contributing_to']]
        """Meta definition for Contributor."""

        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'

    def __str__(self):
        return f'{self.name.username}, {self.contributing_to.name}'

    def save(self,*args, **kwargs):        
        try: 
            # print(self.contributing_to.group)
            group =  self.contributing_to.group
            # from saaco.models import Membership
            membership = Membership.objects.filter(group = group, user = self.name).exists()
            # print(membership)
            if membership: 
                super(Contributor, self).save(*args, **kwargs)
                # get the total contributed to the group so far
                total_contribution = Contributor.objects.filter(contributing_to = self.contributing_to, paid = True).aggregate(Sum('amount'))['amount__sum'] 
                # print(total_contribution)       
                # update contribution.......
                # print(self.contributing_to)
                # print(Contribution.objects.filter( pk = self.contributing_to.pk))
                Contribution.objects.filter( pk = self.contributing_to.pk).update(total = total_contribution)
                # TODO OTHER METHOD
                # contribution = self.contributing_to
                # contribution.total = total_contribution
                # contribution.save()
                

            else: raise NameError('User Doesnt Exist')  

        except: raise NameError('User Doesnt Exist')         
        # super(Contributor, self).save(*args, **kwargs)
        