from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO, StringIO
import os, sys, logging

logger = logging.getLogger(__name__)


class DynamicImageResize(object):
    def __init__(self, width, height, image_field):
        self.width = width
        self.height = height
        self.image_field = image_field
    
    
    def get_resize_image(self):
        THUMB_SIZE = (self.width, self.height)
        image = Image.open(self.image_field)
        image.resize(THUMB_SIZE)
        output = BytesIO()
        image_name, image_extension = os.path.splitext(self.image_field.name)
        image_extension = image_extension.lower()
        image_name = image_name + str(self.width) +"x"+ str(self.height) + image_extension

        if image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif image_extension == '.gif':
            FTYPE = 'GIF'
        elif image_extension == '.png':
            FTYPE = 'PNG'
        
        image.save(output, FTYPE, quality=100)
        output.seek(0)
        return InMemoryUploadedFile(output,'ImageField', "%s.jpg" %image_name, 'image/jpeg', sys.getsizeof(output), None)


