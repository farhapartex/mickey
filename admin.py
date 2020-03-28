from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *
# Register your models here.
def make_category_active(modeladmin, request, queryset):
    queryset.update(active=True)

def make_category_deactivate(modeladmin, request, queryset):
    queryset.update(active=False)

def make_archive(modeladmin, request, queryset):
    queryset.update(archive=True)

def remove_archive(modeladmin, request, queryset):
    queryset.update(archive=False)

def unpublish_post(modeladmin, request, queryset):
    queryset.update(published=False)

def publish_post(modeladmin, request, queryset):
    queryset.update(published=True)



make_category_active.short_description = "Active selected categories"
make_category_deactivate.short_description = "Deactivate selected categories"
make_archive.short_description = "Archive selected post"
remove_archive.short_description = "Publish selected post from archive"
publish_post.short_description = "Publish selected post"
unpublish_post.short_description = "Unpublish selected post"




@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "image","md_image","sm_image", "created_by", "created_at")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = (('parent','name'),'active')
    list_display = ("id", "name", "parent", "active" ,"created_by")
    actions = [make_category_active, make_category_deactivate]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = (('category','archive', 'published'),('title', 'slug'), 'content','short_content', ('cover_image',))
    list_display = ("title", "category", "published", "archive", "created_by")
    search_fields = ['title','category__name','published']
    list_filter = ('category__name', 'published', 'archive')
    actions = [make_archive,remove_archive,publish_post,unpublish_post]

@admin.register(React)
class ReactAdmin(admin.ModelAdmin):
    list_display = ("id","blog", "type", "amount",)
    search_fields = ['blog__title', 'type']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","post", "parent", "name", "created_at")
    fields = (('post','parent'),('name', ), 'body', ('active',))
    list_filter = ('post', 'name', 'active')