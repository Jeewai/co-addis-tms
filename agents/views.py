import random

from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from tickets.models import Agent, UserProfile
from . forms import AgentModelForm
from . mixins import OrganiserAndLoginRequiredMixin

# Create your views here.
class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class OfficialListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/official_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return UserProfile.objects.all()


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.is_official = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be a reviewer.",
            message="You were created as an agent on DJ TMS. Please login to start working.",
            from_email="admin@ilo.org",
            recipient_list=[user.email]
        )
        # agent.organization = self.request.user.userprofile  
        # agent.save()      
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")    

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
 
    def get_success_url(self):
        return reverse("agents:agent-list") 

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

