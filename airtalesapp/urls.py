from django.urls import path, include
from airtalesapp import views
from django.contrib.auth import views as auth_views

app_name = 'airtalesapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('userjournal/', views.journal_entries, name='userjournal'),
    path("save_entry/", views.save_entry, name="save_entry"),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    
    path('like-entry/<int:entry_id>/', views.toggle_like, name='like_entry'),
    
    path('', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='airtalesapp:index'), name='logout'),
    
]
