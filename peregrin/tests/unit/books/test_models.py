from datetime import date
import pytest
from tests.factories.books import BookFactory, ReadingUpdateFactory


@pytest.mark.django_db
def test_book_string():
    title = 'Snakes and Ladders'
    book = BookFactory(title=title, last_page=450)
    assert book.__str__() == title


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
