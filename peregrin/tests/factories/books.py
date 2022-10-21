import factory
from books.models import Book, ReadingUpdate


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book


class ReadingUpdateFactory(factory.django.DjangoModelFactory):
    book = factory.SubFactory(BookFactory)

    class Meta:
        model = ReadingUpdate
