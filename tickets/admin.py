from django.contrib import admin
from . models import User, Ticket, Agent, UserProfile, Status

# Register your models here.

admin.site.register(Status)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Ticket)
admin.site.register(Agent)
