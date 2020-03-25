from django.shortcuts import render
from rest_framework import views, viewsets, generics
from .models import *
from .serializers import *
# Create your views here.

class CategoryAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        return CategoryMinimalSerializer if self.action == "list" else CategorySerializer

class TagReadOnlyAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_class(self):
        return TagMinimalSerializer if self.action == "list" else TagSerializer


class BlogReadOnlyAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        return BlogMinimalSerializer if self.action == "list" else BlogSerializer
    
    def get_queryset(self):
        return Blog.objects.filter(published=True)