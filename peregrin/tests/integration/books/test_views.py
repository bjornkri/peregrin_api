import pytest
from django.urls import reverse
from datetime import date
from rest_framework.test import APIRequestFactory
from books.views import BookViewSet, ReadingUpdateViewSet
from tests.factories.books import BookFactory, ReadingUpdateFactory

factory = APIRequestFactory()


@pytest.mark.django_db
def test_book_list():
    BookFactory(title='First book')
    BookFactory(title='Second book')
    request = factory.get(reverse('book-list'))
    view = BookViewSet.as_view({'get': 'list'})
    response = view(request)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_reading_update_create_with_current_page():
    book = BookFactory(
        title='First book',
        start_date=date(2022, 1, 1)
    )
    request = factory.post(reverse('readingupdate-list'), {
        "book": book.pk, "current_page": 20, "date": date(2022, 1, 1)
    })
    view = ReadingUpdateViewSet.as_view({'post': 'create'})
    response = view(request)
    assert response.data['progress'] == 19


@pytest.mark.django_db
def test_reading_update_update_with_current_page():
    book = BookFactory(
        title='First book',
        start_date=date(2022, 1, 1)
    )
    update = ReadingUpdateFactory(
        book=book, progress=100,
        date=date(2022, 1, 1)
    )
    request = factory.put(
        reverse('readingupdate-detail', kwargs={'pk': update.id}), {
            "current_page": 20,
            "book": book.pk,
        }
    )
    view = ReadingUpdateViewSet.as_view({'put': 'update'})
    response = view(request, pk=update.pk)
    print(response.data)
    assert response.data['progress'] == 19
