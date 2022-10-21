import pytest
from core.utils import import_legacy
from books.models import Book


@pytest.mark.django_db
def test_import_legacy():
    import_legacy([
        {
            "model": "books.book",
            "pk": 1,
            "fields": {
                "title": "Distant Mirror",
                "total": 11856,
                "location_type": 0,
                "start_location": 295,
                "start_date": "2012-12-24",
                "finished": True,
                "target_date": None,
                "user": ["bjornkri"],
                "page_scaling": 20.0
            }
        },
        {
            "model": "history.locationupdate",
            "pk": 15,
            "fields": {
                "book": 1,
                "location": 1012,
                "date": "2012-12-28"
            }
        }
    ])

    assert Book.objects.count() == 1
