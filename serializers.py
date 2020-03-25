from rest_framework import serializers
from .models import *


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


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ("id", "title", "slug", "tags", "content")

class BlogMinimalSerializer(serializers.HyperlinkedModelSerializer):
    short_text = serializers.SerializerMethodField()

    def get_short_text(self, model):
        return model.content[:150]

    class Meta:
        model = Blog
        fields = ("id","url","title", "short_text",)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }