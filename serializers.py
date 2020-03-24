from rest_framework import serializers
from .models import *


class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

class CategorySerializer(serializers.ModelSerializer):
    parent = CategoryMinimalSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source="parent", queryset=Category.objects.all(), write_only=True)
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "parent_id" : {"write_only" : True}
        }