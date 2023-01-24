from rest_framework import status, viewsets
from rest_framework.response import Response

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

    # Overwrite POST to first check if an update exists for the given book and
    # date. If so, update that update instead of creating a new one.
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book', None)
        date = request.data.get('date', None)
        try:
            update = ReadingUpdate.objects.get(book=book_id, date=date)
            serializer = self.get_serializer(update, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReadingUpdate.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
