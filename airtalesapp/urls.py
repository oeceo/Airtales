from django.urls import path
from airtalesapp import views
from .views import save_entry

app_name = 'airtalesapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('userjournal', views.userjournal, name='userjournal'),
    path("save_entry/", views.save_entry, name="save_entry"),
    path("save_entry/", save_entry, name="save_entry"),
   # path("save_entry/", views.save_entry, name="save_entry"),
    #path("save_entry/", views.profile, name="profile"),
]
