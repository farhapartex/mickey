from django.shortcuts import render
from rest_framework import views, viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *
import logging
# Create your views here.

logger = logging.getLogger(__name__)


class CategoryPublicAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        return CategoryMinimalSerializer if self.action == "list" else CategorySerializer

class TagReadOnlyAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagMinimalSerializer


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
            elif post_type == "archive":
                query =  Post.objects.filter(published=True, archive=True)

            if self.request.GET['tag']:
                query =  query.filter(published=True, tags__name=self.request.GET['tag'])
            
            return query
        except:
            query = Post.objects.filter(published=True, archive=False)
            # if self.request.GET['tag']:
            #     query =  Post.objects.filter(published=True, tags__name=self.request.GET['tag'])
            return query


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


class CommentPublicAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        try:
            if not self.request.GET['pid']:
                return Comment.objects.filter(active=True, parent=None)
            elif Comment.objects.filter(post__id=self.request.GET['pid']).exists():
                return Comment.objects.filter(post__id=self.request.GET['pid'], active=True, parent=None)
            else:
                return Comment.objects.none()
        except:
            pass
        return Comment.objects.filter(active=True, parent=None)


class SiteInformationPublicAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = SiteInformation.objects.all()
    serializer_class = SiteInformationFlatSerializer

"""
Admin View API
"""

class PermissionAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated, SystemPermission,)

class GroupAPIView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, GroupPermission,)

    def get_serializer_class(self):
        return GroupMiniSerializer if self.action == "list" else GroupSerializer


class SiteInformationAPIView(viewsets.ModelViewSet):
    queryset = SiteInformation.objects.all()
    serializer_class = SiteInformationSerializer
    permission_classes = (IsAuthenticated, SiteInformationPermission,)

    def create(self, request, *args, **kwargs):
        if DJSiteInformation.objects.all().count()>0:
            return Response({"detail": "More than one information can't be created!"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = (IsAuthenticated, CategoryPermission,)

    def get_serializer_class(self):
        return CategoryMiniAdminSerializer if self.action == "list" else CategoryAdminSerializer

    def destroy(self, request, pk=None):
        if pk is not None:
            category = Category.objects.get(id=pk)
            if category.cat_children.all().count() > 0:
                return Response({"detail": "Category can't be deleted!"}, status=status.HTTP_403_FORBIDDEN)
            else:
                category.delete()
                return Response({"detail" : "Category deleted"}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        queryset = Category.objects.all()

        try:
            if self.request.GET['name']:
                queryset = queryset.filter(name__contains=self.request.GET['name'])
            
            if self.request.GET['parent']:
                queryset = queryset.filter(parent__name__contains=self.request.GET['parent'])
            
            return queryset
        except :
            return queryset


class TagAPIView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, TagPermission)


class MediaAPIView(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsAuthenticated, MediaPermission,)

    def get_serializer_class(self):
        return MediaFlatSerializer if self.action == "list" else MediaSerializer
    

    def get_queryset(self):
        queryset = Media.objects.all()
        try:
            if self.request.GET['name']:
                queryset = queryset.filter(image__contains=self.request.GET['name'])
            return queryset
        except:
            return queryset