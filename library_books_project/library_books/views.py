from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serilizers import *


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True, methods=['get'], url_path='books')
    def books(self, request, pk=None):
        """Получение всех книг по ID автора (передается в URL)"""
        author = self.get_object()
        books = Book.objects.filter(author=author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['get'], url_path='by_genre')
    def by_genre(self, request, pk=None):
        """Получение всех книг по ID жанра (передается в URL)"""
        books = Book.objects.filter(genre_id=pk)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='authors_by_genre')
    def authors_by_genre(self, request, pk=None):
        """Получение всех авторов по ID жанра (передается в URL)"""
        authors = Author.objects.filter(genre_id=pk)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)