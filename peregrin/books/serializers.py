from rest_framework import serializers
from books.models import Book, ReadingUpdate


class BookSerializer(serializers.ModelSerializer):
    current_page = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'first_page', 'last_page',
            'current_page'
        ]


class ReadingUpdateSerializer(serializers.ModelSerializer):
    current_page = serializers.IntegerField(required=False)

    class Meta:
        model = ReadingUpdate
        fields = ['id', 'book', 'date', 'progress', 'current_page']

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

    def validate(self, data):
        progress = data.get('progress', None)
        current_page = data.get('current_page', None)
        if progress is not None and current_page is not None:
            raise serializers.ValidationError(
                "only progress or current_page expected, but not both"
            )
        if self.context['request'].method == 'POST' and (
            progress is None and current_page is None
        ):
            raise serializers.ValidationError(
                "either progress or current_page required"
            )
        return super().validate(data)
