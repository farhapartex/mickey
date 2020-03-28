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


class PostPublishedAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        return PostMinimalSerializer if self.action == "list" else PostSerializer
    
    def get_queryset(self):
        try:
            post_type, query = self.request.GET['type'], None
            if not post_type or post_type == "published":
                query = Post.objects.filter(published=True, archive=False)
            else:
                query =  Post.objects.filter(published=True, archive=True)
            
            return query
        except:
            return Post.objects.filter(published=True, archive=False)


class ReactAPIView(viewsets.ModelViewSet):
    queryset = React.objects.all()
    serializer_class = ReactSerializer

    def get_queryset(self):
        try:
            if not self.request.GET['bid']:
                return React.objects.all()
            elif React.objects.filter(blog__id=int(self.request.GET['bid'])).exists():
                return React.objects.filter(blog__id=self.request.GET['bid'])
        except:
            return React.objects.all()
    
    def get_serializer_class(self):
        return ReactFlatSerializer if self.action == "list" else ReactSerializer