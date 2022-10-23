import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_import_legacy_json():
    call_command(
        "import_legacy_json",
        "./peregrin/tests/integration/books/sample_data.json"
    )
