from django.contrib import admin
from .models import *



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'genre', 'year_publication')
    list_display_links = ('pk', 'title')