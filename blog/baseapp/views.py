from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'baseapp/index.html'