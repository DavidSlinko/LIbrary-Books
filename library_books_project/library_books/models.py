from django.db import models
from .validate_data import validate_year


class Genre(models.Model):
    genre = models.CharField(max_length=50, verbose_name='Жанр')

    def __str__(self):
        return f'Жанр: {self.genre}'
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Author(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Жанр')

    def __str__(self):
        return f'Автор: {self.author}'
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Жанр книги')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор книги')
    title = models.CharField(max_length=200, verbose_name='Название книги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание книги')
    year_publication = models.PositiveIntegerField(validators=[validate_year], verbose_name='Год издания')

    def __str__(self):
        return f'Название: {self.title} - Автор: {self.author}'
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

