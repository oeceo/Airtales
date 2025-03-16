from django.urls import path
from airtalesapp import views

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
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('like-entry/<int:entry_id>/', views.toggle_like, name='like_entry'),
    path('terms/', views.terms, name='terms'),
    path('top-entry/', views.top_entry, name='top-entry'),
    path('topposts/', views.topposts, name='topposts'),
]
