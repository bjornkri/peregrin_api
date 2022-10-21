from rest_framework import viewsets

from books.models import Book, ReadingUpdate
from books.serializers import BookSerializer, ReadingUpdateSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReadingUpdateViewSet(viewsets.ModelViewSet):
    queryset = ReadingUpdate.objects.all()
    serializer_class = ReadingUpdateSerializer
