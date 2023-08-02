from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from model_choices import Status
from project.mixins.models import PKMixin


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.PUBLISHED)


class Post(PKMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[self.publish.year,
                                     self.publish.month,
                                     self.publish.day,
                                     self.slug])


class Comment(PKMixin):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
