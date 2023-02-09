from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    """
    Custom pagination class to limit the number of results per page.
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
