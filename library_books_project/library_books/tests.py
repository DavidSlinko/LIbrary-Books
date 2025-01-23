from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Genre, Book, Author

class GenreAPITestCase(TestCase):
    def setUp(self):
        # Настройка клиента и создание тестовых данных
        self.client = APIClient()
        self.genre1 = Genre.objects.create(genre="Фантастика")
        self.genre2 = Genre.objects.create(genre="Детектив")
        self.valid_payload = {"genre": "Ужасы"}
        self.invalid_payload = {"genre": ""}  # Некорректные данные (пустое поле)

    def test_get_all_genres(self):
        """Тест получения списка всех жанров"""
        response = self.client.get('/api/genres/')  # Отправка GET-запроса на эндпоинт
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа
        self.assertEqual(len(response.data), 2)  # Убедиться, что в ответе 2 жанра
        self.assertEqual(response.data[0]['genre'], self.genre1.genre)  # Проверка имени первого жанра
        self.assertEqual(response.data[1]['genre'], self.genre2.genre)  # Проверка имени второго жанра

    def test_get_single_genre(self):
        """Тест получения одного жанра по ID"""
        response = self.client.get(f'/api/genres/{self.genre1.id}/')  # Отправка GET-запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['genre'], self.genre1.genre)

    def test_get_nonexistent_genre(self):
        """Тест получения несуществующего жанра"""
        response = self.client.get('/api/genres/999/')  # Запрос несуществующего ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_genre(self):
        """Тест создания нового жанра"""
        response = self.client.post('/api/genres/', data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['genre'], self.valid_payload['genre'])

    def test_create_genre_with_invalid_data(self):
        """Тест создания жанра с некорректными данными"""
        response = self.client.post('/api/genres/', data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_genre(self):
        """Тест обновления жанра"""
        update_payload = {"genre": "Триллер"}  # Новое значение жанра
        response = self.client.put(f'/api/genres/{self.genre1.id}/', data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['genre'], "Триллер")  # Убедиться, что жанр обновлен

    def test_partial_update_genre(self):
        """Тест частичного обновления жанра"""
        update_payload = {"genre": "Приключения"}  # Новое значение
        response = self.client.patch(f'/api/genres/{self.genre1.id}/', data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['genre'], "Приключения")  # Проверка изменения

    def test_delete_genre(self):
        """Тест удаления жанра"""
        response = self.client.delete(f'/api/genres/{self.genre1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=self.genre1.id).exists())  # Убедиться, что жанр удален

    def test_delete_nonexistent_genre(self):
        """Тест удаления несуществующего жанра"""
        response = self.client.delete('/api/genres/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorAPITestCase(TestCase):
    def setUp(self):
        # Настройка клиента и создание тестовых данных
        self.client = APIClient()

        # Создаем жанры
        self.genre1 = Genre.objects.create(genre="Фантастика")
        self.genre2 = Genre.objects.create(genre="Детектив")

        # Создаем авторов
        self.author1 = Author.objects.create(author="Артур Кларк", genre=self.genre1)
        self.author2 = Author.objects.create(author="Агата Кристи", genre=self.genre2)

        # Создаем книги
        self.book1 = Book.objects.create(
            title="2001: Космическая одиссея",
            author=self.author1,
            genre=self.genre1,
            year_publication=1968
        )
        self.book2 = Book.objects.create(
            title="Убийство в Восточном экспрессе",
            author=self.author2,
            genre=self.genre2,
            year_publication=1934
        )

        # Данные для тестов
        self.valid_payload = {"author": "Стивен Кинг", "genre": self.genre1.id}
        self.invalid_payload = {"author": "", "genre": ""}


    def test_get_all_authors(self):
        """Тест получения списка всех авторов"""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['author'], self.author1.author)
        self.assertEqual(response.data[1]['author'], self.author2.author)

    def test_get_single_author(self):
        """Тест получения одного автора по ID"""
        response = self.client.get(f'/api/authors/{self.author1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], self.author1.author)

    def test_get_nonexistent_author(self):
        """Тест получения несуществующего автора"""
        response = self.client.get('/api/authors/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_author(self):
        """Тест создания нового автора"""
        response = self.client.post('/api/authors/', data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.valid_payload['author'])

    def test_create_author_with_invalid_data(self):
        """Тест создания автора с некорректными данными"""
        response = self.client.post('/api/authors/', data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_author(self):
        """Тест обновления автора"""
        update_payload = {"author": "Жюль Верн", "genre": self.genre2.id}
        response = self.client.put(f'/api/authors/{self.author1.id}/', data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], "Жюль Верн")
        self.assertEqual(response.data['genre'], self.genre2.id)

    def test_partial_update_author(self):
        """Тест частичного обновления автора"""
        update_payload = {"author": "Герберт Уэллс"}
        response = self.client.patch(f'/api/authors/{self.author1.id}/', data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], "Герберт Уэллс")

    def test_delete_author(self):
        """Тест удаления автора"""
        response = self.client.delete(f'/api/authors/{self.author1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author1.id).exists())

    def test_delete_nonexistent_author(self):
        """Тест удаления несуществующего автора"""
        response = self.client.delete('/api/authors/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_books_by_author(self):
        """Тест получения всех книг автора"""
        response = self.client.get(f'/api/authors/{self.author1.id}/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)


class BookViewSetTestCase(TestCase):
    def setUp(self):
        # Настройка клиента и создание тестовых данных
        self.client = APIClient()

        # Создаем жанры
        self.genre1 = Genre.objects.create(genre="Фантастика")
        self.genre2 = Genre.objects.create(genre="Детектив")

        # Создаем авторов
        self.author1 = Author.objects.create(author="Айзек Азимов", genre=self.genre1)
        self.author2 = Author.objects.create(author="Конан Дойл", genre=self.genre2)

        # Создаем книги
        self.book1 = Book.objects.create(
            title="Основание",
            author=self.author1,
            genre=self.genre1,
            year_publication=1951,
            description="Эпическое научно-фантастическое произведение."
        )
        self.book2 = Book.objects.create(
            title="Этюд в багровых тонах",
            author=self.author2,
            genre=self.genre2,
            year_publication=1887
        )

        # Валидные и невалидные данные
        self.valid_payload = {
            "title": "Дюна",
            "author": self.author1.id,
            "genre": self.genre1.id,
            "year_publication": 1965,
            "description": "Классика научной фантастики."
        }
        self.invalid_payload = {
            "title": "",
            "author": None,
            "genre": None,
            "year_publication": "not_a_year",
            "description": ""
        }

    def test_create_book_with_valid_data(self):
        """Тест на создание книги с валидными данными"""
        response = self.client.post('/api/books/', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "Дюна")

    def test_create_book_with_invalid_data(self):
        """Тест на создание книги с невалидными данными"""
        response = self.client.post('/api/books/', data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 2)

    def test_list_books(self):
        """Тест на получение списка всех книг"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Тест на получение книги по ID"""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_get_books_by_genre(self):
        """Тест на получение книг по жанру через by_genre"""
        response = self.client.get(f'/api/books/{self.genre1.id}/by_genre/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Основание")

    def test_get_authors_by_genre(self):
        """Тест на получение авторов по жанру через authors_by_genre"""
        response = self.client.get(f'/api/books/{self.genre2.id}/authors_by_genre/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], "Конан Дойл")

