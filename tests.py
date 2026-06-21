import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_with_max_length(self, collector):
        collector.add_new_book("Книга с очень длинным названием, которое точно длиннее сорока символов")
        assert len(collector.books_genre) == 0

    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.books_genre
        assert collector.books_genre["Гарри Поттер"] == ""

    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book("Властелин Колец")
        collector.add_new_book("Властелин Колец")
        assert len(collector.books_genre) == 1

    def test_set_book_genre_success(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        assert collector.get_book_genre("Шерлок Холмс") == "Детективы"

    def test_set_book_genre_for_nonexistent_book(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_set_book_genre_with_age_rating(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_book_genre("Оно") == "Ужасы"

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Дюна"]),
        ("Комедии", []),
        ("Детективы", ["Шерлок Холмс"])
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Мой сосед Тоторо")
        collector.set_book_genre("Мой сосед Тоторо", "Мультфильмы")
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        collector.add_new_book("Кошмары")
        collector.set_book_genre("Кошмары", "Детективы")
        
        children_books = collector.get_books_for_children()
        assert "Мой сосед Тоторо" in children_books
        assert "Оно" not in children_books
        assert "Кошмары" not in children_books

    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Три товарища")
        collector.add_book_in_favorites("Три товарища")
        assert "Три товарища" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_not_in_books(self, collector):
        collector.add_book_in_favorites("Отсутствующая книга")
        assert "Отсутствующая книга" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        collector.delete_book_from_favorites("1984")
        assert "1984" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_nonexistent(self, collector):
        collector.add_new_book("Собачье сердце")
        collector.add_book_in_favorites("Собачье сердце")
        collector.delete_book_from_favorites("Отсутствующая книга")
        assert "Собачье сердце" in collector.get_list_of_favorites_books()

    # ============ ТЕСТЫ ДЛЯ get_books_genre ============
    
    def test_get_books_genre_returns_full_dict(self, collector):
        """Проверяет, что get_books_genre возвращает полный словарь книг и жанров"""
        collector.add_new_book("Мастер и Маргарита")
        collector.set_book_genre("Мастер и Маргарита", "Фантастика")
        collector.add_new_book("12 стульев")
        collector.set_book_genre("12 стульев", "Комедии")
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Роман")
        
        books_genre = collector.get_books_genre()
        
        assert books_genre["Мастер и Маргарита"] == "Фантастика"
        assert books_genre["12 стульев"] == "Комедии"
        assert books_genre["Война и мир"] == "Роман"
        assert len(books_genre) == 3

    def test_get_books_genre_empty(self, collector):
        """Проверяет, что get_books_genre возвращает пустой словарь, если книг нет"""
        assert collector.get_books_genre() == {}

    # ============ ТЕСТЫ ДЛЯ get_book_genre ============
    
    def test_get_book_genre_returns_genre_for_existing_book(self, collector):
        """Проверяет, что get_book_genre возвращает жанр для существующей книги"""
        collector.add_new_book("Мастер и Маргарита")
        collector.set_book_genre("Мастер и Маргарита", "Мистика")
        
        genre = collector.get_book_genre("Мастер и Маргарита")
        
        assert genre == "Мистика"

    def test_get_book_genre_returns_none_for_nonexistent_book(self, collector):
        """Проверяет, что get_book_genre возвращает None для несуществующей книги"""
        genre = collector.get_book_genre("Несуществующая книга")
        assert genre is None

    def test_get_book_genre_returns_empty_string_for_book_without_genre(self, collector):
        """Проверяет, что get_book_genre возвращает пустую строку для книги без жанра"""
        collector.add_new_book("Новая книга")
        genre = collector.get_book_genre("Новая книга")
        assert genre == ""

    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []

    def test_add_new_book_exactly_40_chars(self, collector):
        name = "A" * 40
        collector.add_new_book(name)
        assert name in collector.books_genre

    def test_add_new_book_empty_name(self, collector):
        collector.add_new_book("")
        assert len(collector.books_genre) == 0