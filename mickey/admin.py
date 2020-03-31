from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *
import logging

logger = logging.getLogger(__name__)

# Register your models here.

def get_message_bit(rows_updated, model_name):
    if model_name == "category":
        message_bit = "1 category was" if rows_updated == 1 else "%s categories were" % rows_updated
    elif model_name == "post":
        message_bit = "1 post was" if rows_updated == 1 else "%s posts were" % rows_updated
    elif model_name == "tag":
        message_bit = "1 tag was" if rows_updated == 1 else "%s tags were" % rows_updated
    elif model_name == "comment":
        message_bit = "1 comment was" if rows_updated == 1 else "%s comment were" % rows_updated
    
    return message_bit


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "image","md_image","sm_image", "created_by", "created_at")
    fieldsets = (
        ("Required Information", {
            "description": "These fields are required for each Media",
            "fields": (
                ('image', 'image_tag'),
            ),
        }),
        ("Optional Information", {
            'classes': ('collapse',),
            'fields': (
                ('md_image','sm_image'),
            )
        })
    )
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        logger.critical(obj.image.url)
        return format_html('<img src="{}" width="160" height="135"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = (('parent','name'),'active')
    list_display = ("id", "name", "parent", "active" ,"created_by")
    actions = ['make_category_active', 'make_category_deactivate']

    def make_category_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        message_bit = "1 category was" if rows_updated == 1 else "%s categories were" % rows_updated

        self.message_user(request, "%s activated successfully." % message_bit)
    
    def make_category_deactivate(self, request, queryset):
        rows_updated = queryset.update(active=False)
        message_bit = "1 category was" if rows_updated == 1 else "%s categories were" % rows_updated
        self.message_user(request, "%s deactivated successfully." % message_bit)
    
    make_category_active.short_description = "Active selected categories"
    make_category_deactivate.short_description = "Deactivate selected categories"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ("title", "category", "published", "archive", "created_by", "created_at")
    search_fields = ['title','category__name','published']
    list_filter = ('category__name', 'published', 'archive','created_at')
    fieldsets = (
        ("Required Information", {
            "description": "These fields are required for each post",
            "fields": (
                ('category', 'title'), ('content',), ('tags',)
            ),
        }),
        ("Optional Information", {
            'classes': ('collapse',),
            'fields': (
                ('cover_image','image_tag'),
                ('published','archive',),
                ('short_content',),
                ('slug',)
            )
        })
    )
    
    actions = ['make_archive','remove_archive','publish_post','unpublish_post']
    readonly_fields = ('image_tag',)

    def make_archive(self, request, queryset):
        rows_updated = queryset.update(archive=True)
        self.message_user(request, "%s archived successfully." % get_message_bit(rows_updated,'post'))

    def remove_archive(self, request, queryset):
        rows_updated = queryset.update(archive=False)
        self.message_user(request, "%s published from archive successfully." % get_message_bit(rows_updated,'post'))

    def unpublish_post(self, request, queryset):
        rows_updated = queryset.update(published=False)
        self.message_user(request, "%s unpublished successfully." % get_message_bit(rows_updated,'post'))

    def publish_post(self, request, queryset):
        rows_updated = queryset.update(published=True)
        self.message_user(request, "%s published successfully." % get_message_bit(rows_updated,'post'))
    
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" width="160" height="135"/>'.format(obj.cover_image.image.url))
        except:
            return ""
        

    image_tag.short_description = 'Post Image'
    make_archive.short_description = "Archive selected post"
    remove_archive.short_description = "Publish selected post from archive"
    publish_post.short_description = "Publish selected post"
    unpublish_post.short_description = "Unpublish selected post"


@admin.register(React)
class ReactAdmin(admin.ModelAdmin):
    list_display = ("id","blog", "type", "amount",)
    search_fields = ['blog__title', 'type']
    list_filter = ('blog', 'type',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","post", "parent", "name", "active", "created_at")
    fields = (('post','parent'),('name', ), 'body', ('active',))
    list_filter = ('post', 'name', 'active')
    actions = ['make_activate','make_deactivate',]


    def make_activate(self, request, queryset):
        rows_updated = queryset.update(active=True)
        self.message_user(request, "%s activated successfully." % get_message_bit(rows_updated,'comment'))


    def make_deactivate(self, request, queryset):
        rows_updated = queryset.update(active=False)
        self.message_user(request, "%s deactivated successfully." % get_message_bit(rows_updated,'comment'))
    
    make_activate.short_description = "Active selected comments"
    make_deactivate.short_description = "Deactivate selected comments"


@admin.register(DJSiteInformation)
class DJSiteAdmin(admin.ModelAdmin):
    list_display = ("title", "tagline", "created_by")
    fieldsets = (
        ("Required Information", {
            "description": "These fields are required for DJ Site Information",
            "fields": (
                ('title', ),
            ),
        }),
        ("Optional Information", {
            'classes': ('collapse',),
            'fields': (
                ('header_title','tagline',),
                'footer_text'
            )
        })
    )

