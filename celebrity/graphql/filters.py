import django_filters
from django.db.models import Q
from saleor.graphql.core.filters import MetadataFilterBase
from saleor.graphql.core.types.filter_input import FilterInputObjectType

from celebrity import models


def filter_by_query_param(queryset, query, search_fields):
    """Filter queryset according to given parameters.

    Keyword Arguments:
        queryset - queryset to be filtered
        query - search string
        search_fields - fields considered in filtering

    """
    if query:
        query_by = {
            "{0}__{1}".format(field, "icontains"): query for field in search_fields
        }
        query_objects = Q()
        for q in query_by:
            query_objects |= Q(**{q: query_by[q]})
        return queryset.filter(query_objects).distinct()
    return queryset


def filter_celebrity_search(qs, _, value):
    celebrity_fields = ["first_name", "phone_number", "email"]
    qs = filter_by_query_param(qs, value, celebrity_fields)
    return qs


class CelebrityFilter(MetadataFilterBase):
    search = django_filters.CharFilter(method=filter_celebrity_search)

    class Meta:
        model = models.Celebrity
        fields = ["search"]


class CelebrityFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = CelebrityFilter
