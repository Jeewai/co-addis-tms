from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'Official'),
        (2, 'Finance'),
        (3, 'Procurement'),
        (4, 'IT'),
        (5, 'HR'),
    )
    OFFICE_CHOICES = (
        (1, 'Ethiopia'),
        (2, 'Sudan'),
        (3, 'South Sudan'),
        (4, 'Djibouti'),
        (5, 'Somalia'),
    )

    is_organiser = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_official = models.BooleanField(default=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    office = models.PositiveSmallIntegerField(choices=OFFICE_CHOICES, default=1)
    project = models.CharField(max_length=200, null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Ticket(models.Model):

    # STATUS_CHOICES = {
    #     ('Requested', 'Requested'), 
    #     ('Under Review', 'Under Review'), 
    #     ('Approved', 'Approved'),
    # }

    CATEGORY_CHOICES = {
        ('Finance', 'Finance'), 
        ('Procurement', 'Procurement'), 
        ('IT', 'IT')
    }

    ORGANIZATION_CHOICES = {
        ('LORC_ETH', 'LORC_ETH'),
        ('LORC_SUD', 'LORC_SUD')
    }
    title = models.CharField(max_length=200)
    content = models.TextField()
    # organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    organization = models.CharField(choices=ORGANIZATION_CHOICES, max_length=100)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    official = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.ForeignKey("Status", related_name="tickets", null=True, blank=True, on_delete=models.SET_NULL)
    
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.title

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Status(models.Model):
    name = models.CharField(max_length=30) # Requested, Under Review, Approved 
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Official(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    # organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user.email

def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(post_user_created_signal, sender=User)
