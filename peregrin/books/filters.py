from django_filters import rest_framework as filters


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title')
    title__icontains = filters.CharFilter(
        field_name='title', lookup_expr='icontains'
    )
    start_date = filters.DateFromToRangeFilter(field_name='start_date')
    finished = filters.BooleanFilter(field_name='finished')


class ReadingUpdateFilter(filters.FilterSet):
    book = filters.NumberFilter(field_name='book')
    date = filters.DateFromToRangeFilter(field_name='date')
