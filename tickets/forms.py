from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from . models import Ticket, Agent

User = get_user_model()

class TicketModelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'title',
            'content',
            'organization',
            'category',
            'file',
        )

class TicketForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'office', 'project')
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none()) 

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'status',
        )

