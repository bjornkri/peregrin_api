from datetime import date
from django.db import models


class Book(models.Model):
    KINDLE, PAGES = range(2)
    BOOK_TYPE_CHOICES = (
        (KINDLE, 'Kindle Locations'),
        (PAGES, 'Pages')
    )
    title = models.CharField(max_length=255)
    start_location = models.IntegerField(default=1)
    end_location = models.IntegerField()
    start_date = models.DateField(default=date.today)
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
            return update.current_location
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
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} {self.book.title} ({self.progress})"

    class Meta:
        unique_together = ['book', 'date']
        ordering = ['date', 'book']

    @property
    def current_location(self):
        updates = self.book.readingupdate_set.filter(
            date__lte=self.date
        ).aggregate(
            models.Sum('progress')
        )
        progress_sum = updates['progress__sum'] or 0
        return self.book.start_location + progress_sum

    def progress_from_location(self, current_location):
        prev_prog = self.progress
        try:
            prev_update = self.get_previous_by_date(book=self.book)
            progress = current_location - prev_update.current_location
        except ReadingUpdate.DoesNotExist:
            progress = current_location - self.book.start_location
        self.progress = progress
        self.save()
        for update in self.book.readingupdate_set.filter(date__gt=self.date):
            update.progress -= progress - prev_prog
            update.save()
