from datetime import date
import pytest
from tests.factories.books import BookFactory, ReadingUpdateFactory


@pytest.mark.django_db
def test_book_string():
    title = 'Snakes and Ladders'
    book = BookFactory(title=title)
    assert book.__str__() == title


@pytest.mark.django_db
def test_reading_update_string():
    update_date = date(2022, 1, 1)
    title = 'Wuthering Heights'
    update = ReadingUpdateFactory(
        date=update_date,
        progress=10,
        book__title=title,
        book__start_date=update_date
    )
    assert update.__str__() == "2022-01-01 Wuthering Heights (10)"


@pytest.mark.django_db
def test_current_location_for_new_book():
    book = BookFactory()
    assert book.current_location == 1


@pytest.mark.django_db
def test_current_location_for_book_with_updates():
    book = BookFactory(start_date=date(2022, 1, 1))
    ReadingUpdateFactory(book=book, progress=19, date=date(2022, 1, 1))
    ReadingUpdateFactory(book=book, progress=30, date=date(2022, 1, 2))
    assert book.current_location == 50


@pytest.mark.django_db
def test_current_location_for_reading_update():
    book = BookFactory(start_date=date(2022, 1, 1))
    update_1 = ReadingUpdateFactory(
        book=book, progress=19, date=date(2022, 1, 1)
    )
    update_2 = ReadingUpdateFactory(
        book=book, progress=30, date=date(2022, 1, 2)
    )
    assert update_1.current_location == 20
    assert update_2.current_location == 50


@pytest.mark.django_db
def test_update_progress_from_page():
    book = BookFactory(start_date=date(2022, 1, 1))
    update = ReadingUpdateFactory(book=book, date=date(2022, 1, 1))
    update.progress_from_page(20)
    assert update.progress == 19


@pytest.mark.django_db
def test_update_later_progress_from_page():
    book = BookFactory(start_date=date(2022, 1, 1))
    update_1 = ReadingUpdateFactory(book=book, date=date(2022, 1, 1))
    update_2 = ReadingUpdateFactory(book=book, date=date(2022, 1, 2))
    update_2.progress_from_page(50)
    assert update_2.progress == 49
    update_1.progress_from_page(20)
    update_2.refresh_from_db()
    assert update_2.progress == 30
