from rest_framework import serializers
from books.models import Book, ReadingUpdate


class BookSerializer(serializers.ModelSerializer):
    current_location = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'start_location', 'end_location',
            'start_date', 'current_location', 'finished',
        ]


class ReadingUpdateSerializer(serializers.ModelSerializer):
    current_location = serializers.IntegerField()

    class Meta:
        model = ReadingUpdate
        fields = ['id', 'book', 'date', 'progress', 'current_location']
        read_only_fields = ['progress']

    def create(self, validated_data):
        current_location = validated_data.pop('current_location')
        reading_update = ReadingUpdate.objects.create(**validated_data)
        if current_location:
            reading_update.progress_from_location(current_location)
        return reading_update

    def update(self, instance, validated_data):
        current_location = validated_data.pop('current_location', None)
        super().update(instance, validated_data)
        if current_location:
            instance.progress_from_location(current_location)
        return instance
