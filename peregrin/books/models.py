from datetime import date
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    first_page = models.IntegerField(default=1)
    last_page = models.IntegerField()

    def __str__(self):
        return self.title

    @property
    def current_page(self):
        updates = self.readingupdate_set.all().aggregate(
            models.Sum('progress')
        )
        progress_sum = updates['progress__sum'] or 0
        return self.first_page + progress_sum


class ReadingUpdate(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} {self.book.title} ({self.progress})"

    class Meta:
        unique_together = ['book', 'date']

    @property
    def current_page(self):
        updates = self.book.readingupdate_set.filter(
            date__lte=self.date
        ).aggregate(
            models.Sum('progress')
        )
        progress_sum = updates['progress__sum'] or 0
        return self.book.first_page + progress_sum

    def progress_from_page(self, current_page):
        prev_prog = self.progress
        try:
            prev_update = self.get_previous_by_date(book=self.book)
            progress = current_page - prev_update.current_page
        except ReadingUpdate.DoesNotExist:
            progress = current_page - self.book.first_page
        self.progress = progress
        self.save()
        for update in self.book.readingupdate_set.filter(date__gt=self.date):
            update.progress -= progress - prev_prog
            update.save()
