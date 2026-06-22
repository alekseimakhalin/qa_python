import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    """Фикстура создает новый экземпляр BooksCollector для каждого теста"""
    return BooksCollector()


class TestBooksCollector:

    # ========== ТЕСТЫ ДЛЯ add_new_book() ==========
    
    def test_add_new_book_success(self, collector):
        """Тест: книга успешно добавляется"""
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.books_genre
        assert collector.books_genre["Гарри Поттер"] == ""

    def test_add_new_book_duplicate(self, collector):
        """Тест: дубликат книги НЕ добавляется"""
        collector.add_new_book("Властелин Колец")
        collector.add_new_book("Властелин Колец")
        assert len(collector.books_genre) == 1

    def test_add_new_book_with_name_longer_than_40_chars(self, collector):
        """Тест: книга с названием длиннее 40 символов НЕ добавляется"""
        long_name = "Книга с очень длинным названием, которое точно длиннее сорока символов"
        collector.add_new_book(long_name)
        assert len(collector.books_genre) == 0

    def test_add_new_book_exactly_40_chars(self, collector):
        """Тест: книга с названием ровно 40 символов успешно добавляется"""
        name = "A" * 40
        collector.add_new_book(name)
        assert name in collector.books_genre

    def test_add_new_book_empty_name(self, collector):
        """Тест: книга с пустым названием НЕ добавляется"""
        collector.add_new_book("")
        assert len(collector.books_genre) == 0

    # ========== ТЕСТЫ ДЛЯ set_book_genre() ==========
    
    def test_set_book_genre_success(self, collector):
        """Тест: жанр успешно устанавливается для существующей книги"""
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        assert collector.get_book_genre("Шерлок Холмс") == "Детективы"

    def test_set_book_genre_for_nonexistent_book(self, collector):
        """Тест: жанр НЕ устанавливается для несуществующей книги"""
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_set_book_genre_with_age_rating(self, collector):
        """Тест: установка жанра с возрастным рейтингом (Ужасы)"""
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_book_genre("Оно") == "Ужасы"

    # ========== ТЕСТЫ ДЛЯ get_book_genre() ==========
    
    def test_get_book_genre_returns_genre_for_existing_book(self, collector):
        """Тест: get_book_genre возвращает жанр для существующей книги"""
        collector.add_new_book("Мастер и Маргарита")
        collector.set_book_genre("Мастер и Маргарита", "Фантастика")
        genre = collector.get_book_genre("Мастер и Маргарита")
        assert genre == "Фантастика"

    def test_get_book_genre_returns_none_for_nonexistent_book(self, collector):
        """Тест: get_book_genre возвращает None для несуществующей книги"""
        genre = collector.get_book_genre("Несуществующая книга")
        assert genre is None

    def test_get_book_genre_returns_empty_string_for_book_without_genre(self, collector):
        """Тест: get_book_genre возвращает пустую строку для книги без жанра"""
        collector.add_new_book("Новая книга")
        genre = collector.get_book_genre("Новая книга")
        assert genre == ""

    # ========== ТЕСТЫ ДЛЯ get_books_genre() ==========
    
    def test_get_books_genre_returns_full_dict(self, collector):
        """Тест: get_books_genre возвращает полный словарь книг и жанров"""
        collector.add_new_book("Мастер и Маргарита")
        collector.set_book_genre("Мастер и Маргарита", "Фантастика")
        collector.add_new_book("12 стульев")
        collector.set_book_genre("12 стульев", "Комедии")
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Фантастика")
        
        books_genre = collector.get_books_genre()
        
        assert books_genre["Мастер и Маргарита"] == "Фантастика"
        assert books_genre["12 стульев"] == "Комедии"
        assert books_genre["Война и мир"] == "Фантастика"
        assert len(books_genre) == 3

    def test_get_books_genre_empty(self, collector):
        """Тест: get_books_genre возвращает пустой словарь, если книг нет"""
        assert collector.get_books_genre() == {}

    # ========== ТЕСТЫ ДЛЯ get_books_with_specific_genre() ==========
    
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Дюна"]),
        ("Комедии", []),
        ("Детективы", ["Шерлок Холмс"])
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books, collector):
        """Тест: получение книг по жанру (параметризованный)"""
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    # ========== ТЕСТЫ ДЛЯ get_books_for_children() ==========
    
    def test_get_books_for_children_excludes_age_rating_genres(self, collector):
        """Тест: get_books_for_children исключает книги с возрастными жанрами"""
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

    # ========== ТЕСТЫ ДЛЯ add_book_in_favorites() ==========
    
    def test_add_book_in_favorites_success(self, collector):
        """Тест: книга успешно добавляется в избранное"""
        collector.add_new_book("Три товарища")
        collector.add_book_in_favorites("Три товарища")
        assert "Три товарища" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_not_in_books(self, collector):
        """Тест: несуществующая книга НЕ добавляется в избранное"""
        collector.add_book_in_favorites("Отсутствующая книга")
        assert "Отсутствующая книга" not in collector.get_list_of_favorites_books()

    # ========== ТЕСТЫ ДЛЯ delete_book_from_favorites() ==========
    
    def test_delete_book_from_favorites_success(self, collector):
        """Тест: книга успешно удаляется из избранного"""
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        collector.delete_book_from_favorites("1984")
        assert "1984" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_nonexistent(self, collector):
        """Тест: удаление несуществующей книги не влияет на избранное"""
        collector.add_new_book("Собачье сердце")
        collector.add_book_in_favorites("Собачье сердце")
        collector.delete_book_from_favorites("Отсутствующая книга")
        assert "Собачье сердце" in collector.get_list_of_favorites_books()

    # ========== ТЕСТЫ ДЛЯ get_list_of_favorites_books() ==========
    
    def test_get_list_of_favorites_books_empty(self, collector):
        """Тест: get_list_of_favorites_books возвращает пустой список, если избранное пусто"""
        assert collector.get_list_of_favorites_books() == []