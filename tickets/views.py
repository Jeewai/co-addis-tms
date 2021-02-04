from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganiserAndLoginRequiredMixin, OfficialAndLoginRequiredMixin
from . models import Ticket, Agent, Status
from . forms import TicketForm, TicketModelForm, CustomUserCreationForm, AssignAgentForm, TicketStatusUpdateForm


# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class TicketListView(LoginRequiredMixin, generic.ListView):
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"

    # def get_queryset(self):
    #     user = self.request.user
    #     # initial queryset of tickets for the entire organization
    #     if user.is_organiser and not user.is_agent:
    #         queryset =  Ticket.objects.filter(organization=user.userprofile, agent__isnull=False)
    #     elif not user.is_organiser and user.is_agent:
    #         queryset =  Ticket.objects.filter(organization=user.agent.organization, agent__isnull=False)
    #         # filter for the agent that is logged in
    #         queryset =  queryset.filter(agent__user=user)
    #     else:
    #         # filter for the user that is logged in
    #         queryset = Ticket.objects.filter(official__user=user)
    #     return queryset

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser:
            queryset =  Ticket.objects.filter(organization=user.userprofile, agent__isnull=False)
        elif user.is_agent:
            queryset =  Ticket.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset =  queryset.filter(agent__user=user)
        elif user.is_official:
            # filter for the user that is logged in
            queryset = Ticket.objects.filter(official__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser and not user.is_agent:
            queryset =  Ticket.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_tickets": queryset
            })
        return context

def ticket_list(request):
    tickets = Ticket.objects.all()
    context = {
        "tickets": tickets
    }
    return render(request, "tickets/ticket_list.html", context)

class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser:
            queryset =  Ticket.objects.filter(organization=user.userprofile, agent__isnull=False)
        elif user.is_agent:
            queryset =  Ticket.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset =  queryset.filter(agent__user=user)
        elif user.is_official:
            # filter for the user that is logged in
            queryset = Ticket.objects.filter(official=user)
        return queryset


def ticket_detail(request, pk):
    print(pk)
    ticket = Ticket.objects.get(id=pk)
    context = {
        "ticket": ticket
    }
    return render(request, "tickets/ticket_detail.html", context)


class TicketCreateView(OfficialAndLoginRequiredMixin, generic.CreateView):
    template_name = "tickets/ticket_create.html"
    form_class = TicketModelForm

    def get_success_url(self):
        return reverse("tickets:ticket-list")
    
    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.official = self.request.user.userprofile
        # ticket.organization = organization
        ticket.save()

        #TODOL send email
        send_mail(
            subject="A ticket has been created", 
            message="Go to the site to see the new ticket",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(TicketCreateView, self).form_valid(form)

def ticket_create(request):
    form = TicketModelForm()
    if request.method == "POST":
        form = TicketModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/tickets")
    context = {
        "form": form
    }
    return render(request, "tickets/ticket_create.html", context)

class TicketUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tickets/ticket_update.html"
    form_class = TicketModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser:
            queryset =  Ticket.objects.filter(organization=user.userprofile, agent__isnull=False)
        elif user.is_agent:
            queryset =  Ticket.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset =  queryset.filter(agent__user=user)
        elif user.is_official:
            # filter for the user that is logged in
            queryset = Ticket.objects.filter(official=user)
        return queryset
    
    def get_success_url(self):
        return reverse("tickets:ticket-list")

def ticket_update(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketModelForm(instance=ticket)
    if request.method == "POST":
        form = TicketModelForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("/tickets")
    context = {
        "form": form,
        "ticket": ticket
    }
    return render(request, "tickets/ticket_update.html", context)

class TicketDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "tickets/ticket_delete.html"
    queryset = Ticket.objects.all()

    def get_success_url(self):
        return reverse("tickets:ticket-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        return Ticket.objects.filter(organization=user.userprofile)

def ticket_delete(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    return redirect("/tickets")

class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "tickets/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("tickets:ticket-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        ticket = Ticket.objects.get(id=self.kwargs["pk"])
        # status = Status.objects.filter(name="Under Review")
        ticket.agent = agent
        # ticket.status = status
        ticket.save()
        return super(AssignAgentView, self).form_valid(form)

class StatusListView(LoginRequiredMixin, generic.ListView):
    template_name = "tickets/status_list.html"
    context_object_name = "status_list"

    def get_context_data(self, **kwargs):
        context = super(StatusListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser and not user.is_agent:
            queryset =  Ticket.objects.filter(organization=user.userprofile)
        else:
            queryset =  Ticket.objects.filter(organization=user.agent.organization)

        context.update({
            "unassigned_ticket_count": queryset.filter(status__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser and not user.is_agent:
            queryset =  Status.objects.filter(organization=user.userprofile)
        else:
            queryset =  Status.objects.filter(organization=user.agent.organization)
        # elif not user.is_organiser and user.is_agent:
        #     queryset =  Status.objects.filter(organization=user.agent.organization)
        #     # filter for the agent that is logged in
        # else:
        #     # filter for the user that is logged in
        #     queryset = Status.objects.filter(official__user=user)
        return queryset


class StatusDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tickets/status_detail.html"
    context_object_name = "status"

    # def get_context_data(self, **kwargs):
    #     context = super(StatusDetailView, self).get_context_data(**kwargs)
    #     # qs = Ticket.objects.filter(status=self.get_object())
    #     tickets = self.get_object().tickets.all()
    #     context.update({
    #         "tickets": tickets
    #     })
    #     return context
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser and not user.is_agent:
            queryset =  Status.objects.filter(organization=user.userprofile)
        else:
            queryset =  Status.objects.filter(organization=user.agent.organization)
        return queryset


class TicketStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tickets/ticket_status_update.html"
    form_class = TicketStatusUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tickets for the entire organization
        if user.is_organiser and not user.is_agent:
            queryset =  Ticket.objects.filter(organization=user.userprofile)
        else:
            queryset =  Ticket.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("tickets:ticket-detail", kwargs={"pk": self.get_object().id})

# def ticket_update(request, pk):
#     ticket = Ticket.objects.get(id=pk)
#     form = TicketForm()
#     if request.method == "POST":
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             content = form.cleaned_data['content']
#             ticket.title = title
#             ticket.content = content
#             ticket.save()
#             return redirect("/tickets")
#     context = {
#         "form": form,
#         "ticket": ticket
#     }
#     return render(request, "tickets/ticket_update.html", context)



# def ticket_create(request):
#     form = TicketForm()
#     if request.method == "POST":
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             content = form.cleaned_data['content']
#             agent = Agent.objects.first()
#             official = Official.objects.first()
#             Ticket.objects.create(
#                 title = title,
#                 content = content,
#                 agent = agent,
#                 official = official
#             )
#             return redirect("/tickets")
#     context = {
#         "form": form
#     }
#     return render(request, "tickets/ticket_create.html", context)
