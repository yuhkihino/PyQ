from django.urls import path

from . import views


app_name = 'tickets'
urlpatterns = [
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='detail'),
    path('', views.ticket_list, name='list'),
    path('tickets/sell/', views.ticket_sell, name='sell'),
    path('tickets/<int:ticket_id>/manage/',views.ticket_manage, name='manage'),
]
