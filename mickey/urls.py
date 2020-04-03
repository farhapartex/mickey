from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from mickey import views as blog_views

public_router = DefaultRouter()
admin_router = DefaultRouter()

public_router.register(r"categories", blog_views.CategoryPublicAPIView)
public_router.register(r"tags", blog_views.TagReadOnlyAPIView)
public_router.register(r"posts", blog_views.PostPublishedAPIView)
public_router.register(r"reacts", blog_views.ReactAPIView)
public_router.register(r"comments", blog_views.CommentPublicAPIView)
public_router.register(r"site-information", blog_views.SiteInformationPublicAPIView)


admin_router.register(r"permissions", blog_views.PermissionAPIView)
admin_router.register(r"groups", blog_views.GroupAPIView)
admin_router.register(r"categories", blog_views.CategoryAPIView)
admin_router.register(r"tags", blog_views.TagAPIView)
admin_router.register(r"site-information", blog_views.SiteInformationAPIView)
admin_router.register(r"medias", blog_views.MediaAPIView)

urlpatterns = [
    re_path(r"^public/", include(public_router.urls)),
    re_path(r"^admin/", include(admin_router.urls)),
]