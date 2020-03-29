from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import ValidationError
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

"""
Base model is abstract. It is extended by all other models for some default information such as created_at,
created_by, updated_at, updated_by

"""

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


"""
In Media model, only image is main required field. For a single image, medium and small size image is created 
dynamically. medium and small image size can be defined from settings.py. By default medium size is (768,1024)
and small size is (265, 300)

"""
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
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(Base):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Post(Base):
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="blogs", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tag"))
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), max_length=80, blank=True, null=True)
    content = models.TextField(_("Content"))
    short_content = models.TextField(_("Short Content"), blank=True, null=True)
    cover_image = models.ForeignKey(Media, verbose_name=_("Cover Image"), on_delete=models.SET_NULL, blank=True, null=True)
    archive = models.BooleanField(_("Archive"), default=False)
    published = models.BooleanField(_("published"), default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.title) > 80:
                self.slug = self.title[:80]
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        
        if not self.short_content:
            self.short_content = self.content[:150]

        super(Post, self).save(*args, **kwargs)
        instance = Post.objects.get(id=self.id)

        # creating 5 type of reacts for a post, by default each react of any type will be 0

        REACTS = ['like', 'dislike', 'love', 'angry', 'wow']
        if React.objects.filter(blog=instance).exists() == False:
            for react in REACTS:
                React.objects.create(blog=instance, type=react, amount=0)
        

    def __str__(self):
        return self.title if len(self.title) < 40 else self.title[:40]



REACT_CHOICES = (("like", "like"), ("dislike", "Dislike"), ("love", "Love"), ("angry", "Angry"), ("wow", "Wow"))
class React(Base):
    blog = models.ForeignKey(Post, related_name="reacts", on_delete=models.CASCADE)
    type = models.CharField(_("React Type"), choices=REACT_CHOICES, max_length=10)
    amount = models.IntegerField()

    def __str__(self):
        return self.blog.title


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name=_("Post"), related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", verbose_name=_("Parent Comment"), related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "id: "+ str(self.id) + " comment: " +self.body[:10]



"""
Blog site information
"""

class DJSiteInformation(Base):
    title = models.CharField(_("Site Title"), max_length=50)
    tagline = models.CharField(_("Tag Line"), max_length=80, blank=True, null=True)
    header_title = models.CharField(_("Header Title"), max_length=50,blank=True, null=True)
    footer_text = models.CharField(_("Footer Text"), max_length=150, blank=True, null=True)

    def clean(self):
        if not self.id:
            if DJSiteInformation.objects.all().count()==1:
                raise ValidationError(_("More than one site information can't be created"), code='invalid')
    
    class Meta:
        verbose_name_plural = "DJ Site Information"