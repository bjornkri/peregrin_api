import pytest
from django.urls import reverse
from datetime import date
from rest_framework.test import (
    APIRequestFactory, force_authenticate,
)
from books.views import BookViewSet, ReadingUpdateViewSet
from tests.factories.books import BookFactory, ReadingUpdateFactory
from tests.factories.accounts import UserFactory

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
def test_reading_update_create_with_current_location():
    book = BookFactory(
        title='First book',
        start_date=date(2022, 1, 1)
    )
    user = UserFactory()
    request = factory.post(reverse('readingupdate-list'), {
        "book": book.pk, "location": 20, "date": date(2022, 1, 1)
    })
    force_authenticate(request, user=user)
    view = ReadingUpdateViewSet.as_view({'post': 'create'})
    response = view(request)
    assert response.data['location'] == 20


@pytest.mark.django_db
def test_reading_update_update():
    book = BookFactory(
        title='First book',
        start_date=date(2022, 1, 1)
    )
    update = ReadingUpdateFactory(
        book=book,
        location=20,
        date=date(2022, 1, 1)
    )
    user = UserFactory()
    request = factory.post(
        reverse('readingupdate-list'),
        {
            "book": book.pk,
            "location": 50,
            "date": date(2022, 1, 1)
        },
        format='json'
    )
    force_authenticate(request, user=user)
    view = ReadingUpdateViewSet.as_view({'post': 'create'})
    response = view(request, pk=update.pk)
    assert response.data['location'] == 50

    assert book.current_location == 50
