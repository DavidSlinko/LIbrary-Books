from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genre')
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')


urlpatterns = [
    path('', include(router.urls)),
]