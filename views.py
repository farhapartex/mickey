from django.shortcuts import render
from rest_framework import views, viewsets, generics
from .models import *
from .serializers import *
import logging
# Create your views here.

logger = logging.getLogger(__name__)


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


class BlogPublishedAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        return BlogMinimalSerializer if self.action == "list" else BlogSerializer
    
    def get_queryset(self):
        post_type, query = self.request.GET['type'], None
        if not post_type or post_type == "published":
            query = Blog.objects.filter(published=True, archive=False)
        else:
            query =  Blog.objects.filter(published=True, archive=True)
        
        return query