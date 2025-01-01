from rest_framework import pagination
class WatchListPagination(pagination.PageNumberPagination):
    page_size=2
    page_size_query_param='page_size'
    max_page_size=10


class ReviewListPagination(pagination.PageNumberPagination):
    page_size=2 # number of items per page
    page_size_query_param='page_size' # parameter for pagination
    max_page_size=10    # maximum page sizez