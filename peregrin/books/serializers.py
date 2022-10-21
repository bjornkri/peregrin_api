from rest_framework import serializers
from books.models import Book, ReadingUpdate


class BookSerializer(serializers.ModelSerializer):
    current_page = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'start_location', 'end_location',
            'start_date', 'current_page'
        ]


class ReadingUpdateSerializer(serializers.ModelSerializer):
    current_page = serializers.IntegerField()

    class Meta:
        model = ReadingUpdate
        fields = ['id', 'book', 'date', 'progress', 'current_page']
        read_only_fields = ['progress']

    def create(self, validated_data):
        current_page = validated_data.pop('current_page')
        reading_update = ReadingUpdate.objects.create(**validated_data)
        if current_page:
            reading_update.progress_from_page(current_page)
        return reading_update

    def update(self, instance, validated_data):
        current_page = validated_data.pop('current_page', None)
        super().update(instance, validated_data)
        if current_page:
            instance.progress_from_page(current_page)
        return instance
