from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from .media import DynamicImageResize
from .utils import *
from .files import *
import logging, sys
# Create your models here.

logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER_MODEL, null=True, editable=False,
                                   related_name="%(app_label)s_%(class)s_created", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(USER_MODEL, null=True, editable=False,
                                   related_name="%(app_label)s_%(class)s_updated", on_delete=models.CASCADE)
    

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            self.updated_by = user
            if self._state.adding:
                self.created_by = user
        super(Base, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Media(Base):
    image = models.ImageField(_("Image"), storage=fs,upload_to=image_upload_path)
    md_image = models.ImageField(_("Medium Image"), storage=fs,upload_to=md_image_upload_path, blank=True, null=True)
    sm_image = models.ImageField(_("Small Image"), storage=fs,upload_to=sm_image_upload_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            # get image size from settings.py file
            md_size = settings.MID_IMAGE_SIZE
            sm_size = settings.SM_IMAGE_SIZE
        except :
            # if no size get from settings.py, default size will be this
            md_size = (768,1024)
            sm_size = (265, 300)

        if not self.md_image:
            self.md_image = DynamicImageResize(md_size, self.image).get_resize_image()
        if not self.sm_image:
            self.sm_image = DynamicImageResize(sm_size, self.image).get_resize_image()

        super(Media, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.image.name

class Category(Base):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(Base):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Blog(Base):
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="blogs", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tag"))
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), max_length=180, blank=True, null=True)
    content = models.TextField(_("Content"))
    short_content = models.TextField(_("Short Content"), blank=True, null=True)
    cover_image = models.ForeignKey(Media, verbose_name=_("Cover Image"), on_delete=models.SET_NULL, blank=True, null=True)
    archive = models.BooleanField(_("Archive"), default=False)
    published = models.BooleanField(_("published"), default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        
        if not self.short_content:
            self.short_content = self.content[:150]

        super(Blog, self).save(*args, **kwargs)
        instance = Blog.objects.get(id=self.id)
        REACTS = ['like', 'dislike', 'love', 'angry', 'wow']
        if React.objects.filter(blog=instance).exists() == False:
            for react in REACTS:
                React.objects.create(blog=instance, type=react, amount=0)
        

    def __str__(self):
        return self.title


REACT_CHOICES = (("like", "like"), ("dislike", "Dislike"), ("love", "Love"), ("angry", "Angry"), ("wow", "Wow"))
class React(Base):
    blog = models.ForeignKey(Blog, related_name="reacts", on_delete=models.CASCADE)
    type = models.CharField(_("React Type"), choices=REACT_CHOICES, max_length=10)
    amount = models.IntegerField()

    def __str__(self):
        return self.blog.title
        


