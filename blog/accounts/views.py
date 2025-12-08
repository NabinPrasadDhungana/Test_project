from django.views.generic import ListView
from baseapp.models import Blog
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin   
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(TemplateView):
    template_name = 'accounts/registration/registration.html'

class LoginView(TemplateView):
    template_name = 'accounts/registration/login.html'
    success_url = reverse_lazy('index')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.request.user
        context['posts'] = Blog.objects.filter(author=self.request.user).order_by('-created_at')
        context['is_own_profile'] = True
        return context

class PublicProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        try:
            profile_user = User.objects.get(username=username)
            context['profile_user'] = profile_user
            context['posts'] = Blog.objects.filter(author=profile_user).order_by('-created_at')
            context['is_own_profile'] = self.request.user.is_authenticated and self.request.user == profile_user
        except User.DoesNotExist:
            from django.http import Http404
            raise Http404("User not found")
        return context
    
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
    
class MyPostsView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'accounts/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)
    
class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'