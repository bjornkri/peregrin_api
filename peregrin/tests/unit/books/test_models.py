import pytest
from tests.factories.books import BookFactory


@pytest.mark.django_db
def test_book_string():
    title = 'Snakes and Ladders'
    book = BookFactory(title=title, last_page=450)
    assert book.__str__() == title


@pytest.mark.django_db
def test_current_page():
    book = BookFactory(title='Snakes and Ladders', first_page=1, last_page=450)
    assert book.current_page == 1
