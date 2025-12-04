from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView
from .views import RegisterView, LoginView, ProfileView, PublicProfileView, MyPostsView, SettingsView
from .admin_views import (
    AdminDashboardView, 
    AdminUserListView, 
    AdminBlogListView, 
    AdminCategoryListView, 
    AdminCommentListView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('settings/', SettingsView.as_view(), name='settings'),
    
    # Admin Dashboard URLs
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin-dashboard/blogs/', AdminBlogListView.as_view(), name='admin_blogs'),
    path('admin-dashboard/categories/', AdminCategoryListView.as_view(), name='admin_categories'),
    path('admin-dashboard/comments/', AdminCommentListView.as_view(), name='admin_comments'),
]

