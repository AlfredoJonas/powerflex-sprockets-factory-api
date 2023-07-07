from django.db.models import Q
from functools import reduce


def query_filter_to_paginated_api_view(allowed_filters, filter_conditions, queryset):
    # Apply filter conditions one by one
    for condition in filter_conditions:
        key, value = condition.split(":")

        # Handle different filter conditions based on the key
        if key in allowed_filters:
            queryset = queryset.filter(**{key: value})
    return queryset


def query_order_to_paginated_api_view(
    allowed_order_filters, ordering_conditions, queryset
):
    # Apply ordering conditions one by one
    allowed = lambda x: x in allowed_order_filters
    for condition in ordering_conditions:
        if condition.startswith("-"):
            field = condition[1:]  # Remove the leading '-' for descending order
            if allowed(field):
                queryset = queryset.order_by(f"-{field}")
        elif allowed(condition):
            queryset = queryset.order_by(condition)
    return queryset
