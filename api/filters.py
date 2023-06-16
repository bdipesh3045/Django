import django_filters
from .models import Blogs


class BlogFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    username = django_filters.CharFilter(lookup_expr="icontains")
    date = django_filters.DateFilter()
    email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Blogs
        fields = ["name", "username", "date", "email"]
