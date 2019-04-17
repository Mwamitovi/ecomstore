# catalog/models.py
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True,
        help_text='Unique value for product page URL, created from name.'
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        "Meta Keywords", max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag.'
    )
    meta_description = models.CharField(
        "Meta Description", max_length=255,
        help_text='Content for description meta tag.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'catalog_category', (), {'category_slug': self.slug}

