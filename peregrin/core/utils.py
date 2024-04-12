import os
from books.models import Book, ReadingUpdate
from django.contrib.auth import get_user_model

User = get_user_model()


def import_legacy(js):
    # Get or create the user from DEFAULT_USERNAME in env
    username = os.environ.get('DEFAULT_USER_USERNAME', None)
    user = None
    if username:
        user, created = User.objects.get_or_create(
            username=username,
        )
        if created:
            user.set_password(os.environ.get('DEFAULT_USER_PASSWORD'))
            user.save()
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
                type=record['fields']['location_type'],
                user=user
            )
        elif record['model'] == 'history.locationupdate':
            ReadingUpdate.objects.create(
                id=record['pk'],
                book_id=record['fields']['book'],
                location=record['fields']['location'],
                date=record['fields']['date']
            )
