from rest_framework import serializers
from books.models import Book, ReadingUpdate


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'type', 'start_location', 'end_location',
            'start_date', 'target_date', 'finished',
        ]


class ReadingUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingUpdate
        fields = ['id', 'book', 'date', 'location']
