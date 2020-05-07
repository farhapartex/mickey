from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .models import *
from .exceptions import *


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "username",)

class MediaFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("id", "image", "md_image", "sm_image")

class CategoryMinimalSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, model):
        if model.parent is None:
            return None
        else:
            return {
                "id" : model.parent.id,
                "name" : model.parent.name
            }
    class Meta:
        model = Category
        fields = ("id", "name", "parent")

class CategorySerializer(serializers.ModelSerializer):
    parent = CategoryMinimalSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source="parent", queryset=Category.objects.all(), write_only=True)

    def create(self, validated_data):
        validated_data['active'] = True
        return Category.objects.create(**validated_data)

    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "parent_id" : {"write_only" : True}
        }


class TagMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

class ReactSerializer(serializers.ModelSerializer):

    def create(self, validate_data):
        validate_data['amount'] = 0
        return React.objects.create(**validate_data)

    def update(self, instance, validated_data):
        instance.amount = instance.amount + 1
        instance.save()
        return instance
        
    class Meta:
        model = React
        fields = ("id", "blog", "type", "amount")
        extra_kwargs = {
            "amount" : {"read_only": True}
        }


class ReactMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ("type", "amount")

class ReactFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ("id","type", "amount")


class PostSerializer(serializers.ModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    updated_by = UserMiniSerializer(read_only=True)
    reacts = ReactMinimalSerializer(read_only=True, many=True)
    cover_image = MediaFlatSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        

class PostMinimalSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    tags = TagMinimalSerializer(read_only=True, many=True)
    total_react = serializers.SerializerMethodField()
    total_comment = serializers.SerializerMethodField()
    cover_image = MediaFlatSerializer(read_only=True)

    def get_total_react(self, model):
        return React.objects.filter(blog=model).aggregate(Sum('amount'))['amount__sum']
    
    def get_total_comment(self, model):
        return model.comments.all().count()


    class Meta:
        model = Post
        fields = ("id","url","title", "tags","slug", "total_react", "total_comment", "short_content", "cover_image", "created_by", "created_at")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }



class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data["active"] = True
        parent =  validated_data.get("parent")
        post = validated_data.get("post")
        if parent:
            if parent.parent:
                raise SerializerException('Comment creation denied','username',"comment", status_code=status.HTTP_403_FORBIDDEN)
            if parent.post.id != post.id:
                raise SerializerException('Comment post & parent post is not same', "comment", status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        fields = ("id", "name", "body", "post","parent", "children", "created_at")


class SiteInformationFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInformation
        fields = ("title", "tagline", "header_title", "footer_text")



# Private/ admin API serializer

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class GroupMiniSerializer(serializers.ModelSerializer):
    total_permission = serializers.SerializerMethodField()

    def get_total_permission(self, model):
        return model.permissions.all().count()

    class Meta:
        model = Group
        fields = ("id", "name", "total_permission")


class SiteInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInformation
        fields = "__all__"

class CategoryAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class CategoryMiniAdminSerializer(serializers.ModelSerializer):
    total_child = serializers.SerializerMethodField()

    def get_total_child(self, model):
        return model.cat_children.all().count()

    class Meta:
        model = Category
        fields = ("id", "parent", "name", "total_child")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "created_by", "created_at")


class TagFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "created_by", "created_at")


class MediaSerializer(serializers.ModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    updated_by = UserMiniSerializer(read_only=True)
    md_image = serializers.SerializerMethodField()
    sm_image = serializers.SerializerMethodField()
    
    def get_md_image(self, model):
        return {
            "name" : model.image.name.split("/")[1],
            "url" : model.image.url
        }
    
    def get_sm_image(self, model):
        return {
            "name" : model.image.name.split("/")[1],
            "url" : model.image.url
        }

    class Meta:
        model = Media
        fields = "__all__"
        extra_kwargs = {
            "md_image" : {"read_only" : True},
            "sm_image" : {"read_only" : True}
        }


class MediaFlatSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    md_image = serializers.SerializerMethodField()
    sm_image = serializers.SerializerMethodField()

    def get_image(self, model):
        return {
            "name" : model.image.name.split("/")[1],
            "url" : model.image.url
        }
    
    def get_md_image(self, model):
        return {
            "name" : model.image.name.split("/")[1],
            "url" : model.image.url
        }
    
    def get_sm_image(self, model):
        return {
            "name" : model.image.name.split("/")[1],
            "url" : model.image.url
        }

    class Meta:
        model = Media
        fields = ("id", "image", "md_image", "sm_image")
