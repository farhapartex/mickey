from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

SYS_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings.MEDIA_ROOT = os.path.join(SYS_BASE_DIR, "media/blog/images/")

fs = FileSystemStorage(location="media/blog/images/")

def cover_image_upload_path(instance, filename):
    return "full/post_{0}/{1}".format(instance.id, filename)

def m_cover_image_upload_path(instance, filename):
    return "medium/post_{0}/{1}".format(instance.id, filename)

def sm_cover_image_upload_path(instance, filename):
    return "small/_post_{0}/{1}".format(instance.id, filename)

def blog_image_upload_path(instance, filename):
    return "post_{0}/{1}".format(instance.id, filename)