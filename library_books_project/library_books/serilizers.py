from rest_framework.serializers import ModelSerializer
from .models import *


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author', 'genre']


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'genre', 'author', 'title', 'description', 'year_publication']