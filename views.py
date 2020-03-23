from django.shortcuts import render
from rest_framework import views, viewsets, generics
from .models import *
from .serializers import *
# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
