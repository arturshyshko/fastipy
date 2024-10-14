from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination


class PageNumberPagination(DRFPageNumberPagination):
    """Overriding standard DRF pagination to set default limits."""

    page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 1000
