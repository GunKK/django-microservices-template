from rest_framework import pagination
from rest_framework.response import Response
from urllib.parse import urlparse, urlunparse

class CustomPaginator(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size' 
    max_page_size = 100

    def get_next_link(self):
        return super().get_next_link()

    def get_previous_link(self):
        return super().get_previous_link()

    def get_paginated_response(self, data):

        return Response({
            "status" : True,
            "data": data,
            "pagination": {
                "total_items": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link()
            }
        })
    
