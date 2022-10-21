import factory
from books.models import Book


class BookFactory(factory.Factory):

    class Meta:
        model = Book
