from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import os, sys


class DynamicImageResize(object):
    def __init__(self, width, height, image_field):

        self.width = width
        self.height = height
        self.image_field = image_field

    def get_resize_image(self):

        IMAGE_SIZE = (self.width, self.height)
        file = storage.open(self.image_field.name, "r")
        try:
            image = Image.open(file)
        except:
            return False
        
        image.resize(IMAGE_SIZE, Image.ANTIALIAS)
        file.close()

        resize_image_name, resize_image_extension = os.path.splitext(self.image_field.name)
        resize_image_extension = resize_image_extension.lower()
        resize_image_name = resize_image_name + "_" + str(self.width) + "x" + str(self.height) + resize_image_extension

        FTYPE = ""

        if resize_image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif resize_image_extension == '.gif':
            FTYPE = 'GIF'
        elif resize_image_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        
        resize_image = BytesIO()
        image.save(resize_image, format=FTYPE, quality=100)
        resize_image.seek(0)
        # self.thumbnail_field.save(resize_image_name, ContentFile(resize_image.read()), save=False)
        resize_image.close()

        return InMemoryUploadedFile(resize_image,'ImageField', resize_image_name, 'image/jpeg', sys.getsizeof(resize_image), None)