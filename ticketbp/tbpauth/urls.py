from django.urls import path

from . import views


app_name = 'tbpauth'
urlpatterns = [
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/edit/', views.mypage_edit, name='mypage_edit'),
]
