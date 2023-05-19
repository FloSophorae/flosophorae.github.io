from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image

class ArticleCategory(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    father = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class Article(models.Model):
    category = models.ForeignKey(
        ArticleCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = TaggableManager(blank=True)

    title = models.CharField(max_length=100)
    body = models.TextField()

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title