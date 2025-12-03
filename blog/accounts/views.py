from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()

# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     model = User

# class ProfileView(TemplateView):
#     template_name = 'accounts/user_detail.html'

