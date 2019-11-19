from django.contrib import admin

from polls.models import Column, Column_child, Article
# Register your models here.

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display=('id', 'name')


@admin.register(Column_child)
class ChildAdmin(admin.ModelAdmin):
    list_display=('id', 'name')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'content', 'created_at', 'author', 'img', 'column')