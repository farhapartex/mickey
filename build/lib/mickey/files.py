from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

SYS_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# settings.MEDIA_ROOT = os.path.join(SYS_BASE_DIR, "media/images/")

fs = FileSystemStorage(location="media/images/")

def image_upload_path(instance, filename):
    return "full/{1}".format(instance.id,filename)

def md_image_upload_path(instance, filename):
    return "medium/{1}".format(instance.id,filename)

def sm_image_upload_path(instance, filename):
    return "small/{1}".format(instance.id,filename)