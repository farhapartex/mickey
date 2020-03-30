from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO, StringIO
import os, sys, logging

logger = logging.getLogger(__name__)


class DynamicImageResize(object):
    def __init__(self, image_size, image_field):
        self.width, self.height = image_size
        self.image_field = image_field
    
    
    def get_resize_image(self):
        aspect_ratio = self.image_field.width / float(self.image_field.height)
        new_height = int(self.width / aspect_ratio)
        
        if new_height < self.height:
            final_width = self.width
            final_height = new_height
        else:
            final_width = int(aspect_ratio * self.height)
            final_height = self.height

        THUMB_SIZE = (final_width, final_height)
        image = Image.open(self.image_field)

        exif = None
        if 'exif' in image.info:
            exif = image.info['exif']

        image = image.resize(THUMB_SIZE, Image.ANTIALIAS)
        output = BytesIO()
        image_name, image_extension = os.path.splitext(self.image_field.name)
        image_extension = image_extension.lower()
        image_name = image_name + str(final_width) +"x"+ str(final_height) + image_extension

        if image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif image_extension == '.gif':
            FTYPE = 'GIF'
        elif image_extension == '.png':
            FTYPE = 'PNG'
        
        if exif:
            image.save(output, format=FTYPE, exif=exif, quality=90)
        else:
            image.save(output, FTYPE, quality=90)

        output.seek(0)

        return InMemoryUploadedFile(output,'ImageField', image_name, 'image/jpeg', sys.getsizeof(output), None)


