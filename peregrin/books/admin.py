from django.contrib import admin
from books.models import Book, ReadingUpdate


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(ReadingUpdate)
class ReadingUpdateAdmin(admin.ModelAdmin):
    pass
