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
        location=10,
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
    ReadingUpdateFactory(book=book, location=20, date=date(2022, 1, 1))
    ReadingUpdateFactory(book=book, location=50, date=date(2022, 1, 2))
    assert book.current_location == 50


@pytest.mark.django_db
def test_last_reading_update_with_no_updates():
    current_date = date(2022, 1, 1)
    book = BookFactory(start_date=current_date)
    assert book.last_reading_update == current_date


@pytest.mark.django_db
def test_last_reading_update_with_one_update():
    current_date = date(2022, 1, 1)
    update = ReadingUpdateFactory(date=current_date)
    assert update.book.last_reading_update == current_date


@pytest.mark.django_db
def test_last_reading_update_with_out_of_order_updates():
    current_date = date(2022, 1, 3)
    update = ReadingUpdateFactory(date=current_date)
    ReadingUpdateFactory(date=date(2022, 1, 1), book=update.book)
    ReadingUpdateFactory(date=date(2022, 1, 2), book=update.book)
    assert update.book.last_reading_update == current_date


@pytest.mark.django_db
def test_progress_calculation():
    book = BookFactory(
        start_location=1,
        end_location=100,
        start_date=date(2022, 1, 1)
    )
    ru1 = ReadingUpdateFactory(
        book=book,
        location=20,
        date=date(2022, 1, 1)
    )
    ru2 = ReadingUpdateFactory(
        book=book,
        location=50,
        date=date(2022, 1, 2)
    )
    assert ru1.progress == 19
    assert ru2.progress == 30
