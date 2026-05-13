from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('tickets/', views.ticket_list, name='ticket_list'),

    path('tickets/create/', views.create_ticket, name='create_ticket'),

    path('tickets/update/<int:id>/', views.update_ticket, name='update_ticket'),

    path('tickets/delete/<int:id>/', views.delete_ticket, name='delete_ticket'),

]

