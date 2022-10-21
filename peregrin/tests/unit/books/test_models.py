import pytest
from tests.factories.books import BookFactory


@pytest.mark.django_db
def test_current_page():
    book = BookFactory(title='Snakes and Ladders')
    assert book.title == 'Snakes and Ladders'
