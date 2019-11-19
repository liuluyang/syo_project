from django.db import models
import django
# Create your models here.

class Img(models.Model):

    img_url = models.ImageField(upload_to='img', max_length=255)
    text = models.TextField(null=True)
    desc = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(default=django.utils.timezone.now)

    name = models.CharField(max_length=255, null=True)

    tags = models.CharField(max_length=255, null=True, default='xs')

    likes = models.IntegerField(default=0)

    followers = models.UUIDField(null=True)

# class Te(models.Model):
#     name = models.CharField(max_length=255, null=True)


class Column(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name='父栏目')
    def __str__(self):
        return self.name

class Column_child(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name='子栏目')
    column = models.ForeignKey(Column, on_delete=True)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    author = models.CharField(max_length=255, null=True)
    img = models.ImageField(upload_to='article_img', max_length=255)
    column = models.ForeignKey(Column_child, on_delete=True)
    def __str__(self):
        return self.title


