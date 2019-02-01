from django.urls import path

from . import views


app_name = 'cart'
urlpatterns = [
    path('tickets/<int:ticket_id>/delete', views.cart_delete, name='delete'),
    path('', views.cart_list, name='list'),
]
