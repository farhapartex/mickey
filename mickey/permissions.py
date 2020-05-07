from django.contrib.auth.models import Group, Permission
from rest_framework import permissions
from .models import *

def _check_has_permission(request, model, view):
    perm_str = ""
    if view.action == "list":
        perm_str = model._meta.app_label + ".view_" + model.__name__.lower()
    elif view.action == "create":
        perm_str = model._meta.app_label + ".add_" + model.__name__.lower()
    elif view.action == "update":
        perm_str = model._meta.app_label + ".change_" + model.__name__.lower()
    elif view.action == "retrieve":
        perm_str = model._meta.app_label + ".view_" + model.__name__.lower()
    elif view.action == "destroy":
        perm_str = model._meta.app_label + ".delete_" + model.__name__.lower()
        
    return request.user.has_perm(perm_str)


class SystemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request,Permission, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request,Permission, view)

class GroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request,Group, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request,Group, view)


class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request,Category, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request,Category, view)

class TagPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request, Tag, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request, Tag, view)


class SiteInformationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request, SiteInformation, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request, SiteInformation, view)


class MediaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_has_permission(request, Media, view)

    
    def has_object_permission(self, request, view, obj):
        return _check_has_permission(request, Media, view)