from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO, StringIO
import os, sys, logging

logger = logging.getLogger(__name__)


class DynamicImageResize(object):
    def __init__(self, width, height, image_field, resize_field):

        self.width = width
        self.height = height
        self.image_field = image_field
        self.thumbnail_field = resize_field
    
    
    # def make_thumbnail(self):
    #     THUMB_SIZE = (self.width, self.height)

    #     fh = storage.open(self.image_field.name, 'r') 
    #     try:
    #         image = Image.open(self.image_field)
    #     except:
    #         return False

    #     image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    #     fh.close()

    #     thumb_name, thumb_extension = os.path.splitext(self.image_field.name)
    #     thumb_extension = thumb_extension.lower()
    #     thumb_filename = thumb_name + str(self.width) +"x"+ str(self.height) + thumb_extension
    #     thumb_filename = thumb_filename.split("/")[1]

    #     if thumb_extension in ['.jpg', '.jpeg']:
    #         FTYPE = 'JPEG'
    #     elif thumb_extension == '.gif':
    #         FTYPE = 'GIF'
    #     elif thumb_extension == '.png':
    #         FTYPE = 'PNG'
    #     else:
    #         return False

    #     temp_thumb = BytesIO()
    #     image.save(temp_thumb, FTYPE)
    #     temp_thumb.seek(0)
    #     self.thumbnail_field.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    #     temp_thumb.close()

    #     return True


