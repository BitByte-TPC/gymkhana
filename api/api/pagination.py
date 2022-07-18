from rest_framework.pagination import LimitOffsetPagination


class APILimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 50
