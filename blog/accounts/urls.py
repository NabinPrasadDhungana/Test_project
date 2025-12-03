from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView
from .views import RegisterView, LoginView, ProfileView, MyPostsView, SettingsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
