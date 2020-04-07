from django.conf import settings
from rest_framework import pagination


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = getattr(settings, "OBM_PAGINATION_LIMIT", 100)
    max_limit = getattr(settings, "OBM_PAGINATION_MAX_LIMIT", 500)
