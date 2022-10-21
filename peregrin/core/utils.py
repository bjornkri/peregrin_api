
from books.serializers import Book, ReadingUpdateSerializer


def import_legacy(js):
    for record in js:
        if record['model'] == "books.book":
            Book.objects.create(
                id=record['pk'],
                title=record['fields']['title'],
                end_location=record['fields']['total'],
                start_location=record['fields']['start_location'],
                start_date=record['fields']['start_date'],
                finished=record['fields']['finished']
            )
        elif record['model'] == 'history.locationupdate':
            update = ReadingUpdateSerializer(data={
                    "book": record['fields']['book'],
                    "current_page": record['fields']['location'],
                    "date": record['fields']['date']
                }
            )
            if update.is_valid():
                update.save()
