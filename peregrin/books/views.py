from rest_framework import viewsets

from books.filters import BookFilter, ReadingUpdateFilter
from books.models import Book, ReadingUpdate
from books.serializers import BookSerializer, ReadingUpdateSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter


class ReadingUpdateViewSet(viewsets.ModelViewSet):
    queryset = ReadingUpdate.objects.all()
    serializer_class = ReadingUpdateSerializer
    filterset_class = ReadingUpdateFilter
