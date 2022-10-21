from datetime import date
import pytest
from tests.factories.books import BookFactory, ReadingUpdateFactory


@pytest.mark.django_db
def test_book_string():
    title = 'Snakes and Ladders'
    book = BookFactory(title=title, last_page=450)
    assert book.__str__() == title


@pytest.mark.django_db
def test_reading_update_string():
    update_date = date(2022, 1, 1)
    title = 'Wuthering Heights'
    update = ReadingUpdateFactory(
        date=update_date,
        progress=10,
        book__title=title,
        book__last_page=300
    )
    assert update.__str__() == "2022-01-01 Wuthering Heights (10)"


@pytest.mark.django_db
def test_current_page_for_new_book():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    assert book.current_page == 1


@pytest.mark.django_db
def test_current_page_for_book_with_updates():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    ReadingUpdateFactory(book=book, progress=19, date=date(2022, 1, 1))
    ReadingUpdateFactory(book=book, progress=30, date=date(2022, 1, 2))
    assert book.current_page == 50


@pytest.mark.django_db
def test_current_page_for_reading_update():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    update_1 = ReadingUpdateFactory(
        book=book, progress=19, date=date(2022, 1, 1)
    )
    update_2 = ReadingUpdateFactory(
        book=book, progress=30, date=date(2022, 1, 2)
    )
    assert update_1.current_page == 20
    assert update_2.current_page == 50


@pytest.mark.django_db
def test_update_progress_from_page():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    update = ReadingUpdateFactory(book=book, date=date(2022, 1, 1))
    update.progress_from_page(20)
    assert update.progress == 19


@pytest.mark.django_db
def test_update_later_progress_from_page():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    update_1 = ReadingUpdateFactory(book=book, date=date(2022, 1, 1))
    update_2 = ReadingUpdateFactory(book=book, date=date(2022, 1, 2))
    update_2.progress_from_page(50)
    assert update_2.progress == 49
    update_1.progress_from_page(20)
    update_2.refresh_from_db()
    assert update_2.progress == 30
