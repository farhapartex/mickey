from django.conf import settings
from django.db.models import Sum
from rest_framework import serializers
from .models import *


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "username",)

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
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "parent_id" : {"write_only" : True}
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class TagMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ReactMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ("type", "amount")


class BlogSerializer(serializers.ModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    updated_by = UserMiniSerializer(read_only=True)
    reacts = ReactMinimalSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = "__all__"
        # extra_kwargs = {
        #     "reacts" : {"read_only": True}
        # }

class BlogMinimalSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    tags = TagMinimalSerializer(read_only=True, many=True)
    reacts = serializers.SerializerMethodField()

    def get_reacts(self, model):
        return {
            "total" : React.objects.filter(blog=model).aggregate(Sum('amount'))['amount__sum']
        }


    class Meta:
        model = Blog
        fields = ("id","url","title", "tags","slug", "reacts", "short_content", "cover_image", "created_by", "created_at")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }