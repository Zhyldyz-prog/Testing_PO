
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/', blank=True)
    description = models.TextField()
    author = models.CharField(
        max_length=100,
        default='Ivanov Ivan'
    )
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titleпше
