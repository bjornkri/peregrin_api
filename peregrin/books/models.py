from datetime import date
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class Book(models.Model):
    KINDLE, PAGES = range(2)
    BOOK_TYPE_CHOICES = (
        (KINDLE, 'Kindle Locations'),
        (PAGES, 'Pages')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=255)
    start_location = models.IntegerField(default=1)
    end_location = models.IntegerField()
    start_date = models.DateField(default=date.today)
    target_date = models.DateField(blank=True, null=True)
    finished = models.BooleanField(default=False)
    type = models.PositiveSmallIntegerField(
        choices=BOOK_TYPE_CHOICES, default=PAGES
    )

    def __str__(self):
        return self.title

    @property
    def current_location(self):
        update = self.readingupdate_set.last()
        if update:
            return update.location
        return self.start_location

    @property
    def last_reading_update(self):
        update = self.readingupdate_set.last()
        if update:
            return update.date
        return self.start_date


class ReadingUpdate(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    location = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} {self.book.title} ({self.location})"

    class Meta:
        unique_together = ['book', 'date']
        ordering = ['date', 'book']

    @property
    def progress(self):
        try:
            prev_update = self.get_previous_by_date(book=self.book)
            return self.location - prev_update.location
        except ReadingUpdate.DoesNotExist:
            return self.location - self.book.start_location
        return 0
