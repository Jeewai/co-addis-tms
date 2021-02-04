from django.urls import path
from . views import (
    ticket_list, ticket_detail, ticket_create, ticket_update, ticket_delete,
    TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView, TicketDeleteView, 
    AssignAgentView, StatusListView, StatusDetailView, TicketStatusUpdateView
)

app_name = "tickets"

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/status/', TicketStatusUpdateView.as_view(), name='ticket-status-update'),
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('status/', StatusListView.as_view(), name='status-list'),
    path('status/<int:pk>/', StatusDetailView.as_view(), name='status-detail')
]