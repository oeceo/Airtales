from django.urls import path
from airtalesapp import views

app_name = 'airtalesapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
