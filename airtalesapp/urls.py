from django.urls import path, include
from airtalesapp import views
from django.contrib.auth import views as auth_views

app_name = 'airtalesapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('userjournal/', views.journal_entries, name='userjournal'),
    path("save_entry/", views.save_entry, name="save_entry"),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('like-entry/<int:entry_id>/', views.toggle_like, name='like_entry'),
    path('report-entry/<int:entry_id>/', views.report_entry, name='report_entry'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('terms/', views.terms, name='terms'),
    path('top-entry/', views.top_entry, name='top-entry'),
    path('topposts/', views.topposts, name='topposts'),
    path('', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='airtalesapp:index'), name='logout'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]
