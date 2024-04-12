
from books.models import Book, ReadingUpdate


def import_legacy(js):
    for record in js:
        if record['model'] == "books.book":
            Book.objects.create(
                id=record['pk'],
                title=record['fields']['title'],
                end_location=record['fields']['total'],
                start_location=record['fields']['start_location'],
                start_date=record['fields']['start_date'],
                target_date=record['fields']['target_date'],
                finished=record['fields']['finished'],
                type=record['fields']['location_type']
            )
        elif record['model'] == 'history.locationupdate':
            ReadingUpdate.objects.create(
                id=record['pk'],
                book_id=record['fields']['book'],
                location=record['fields']['location'],
                date=record['fields']['date']
            )
