from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.text import slugify
from .utils import *
import logging
# Create your models here.

USER_MODEL = settings.AUTH_USER_MODEL

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
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="blogs", on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tag"))
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), blank=True, null=True)
    content = models.TextField(_("Content"))
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        super(Blog, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.title
        


