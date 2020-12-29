from django.utils.deprecation import MiddlewareMixin
from uuid import uuid4
# from django.http import get_response

class LogMiddleware(MiddlewareMixin):
    """ Class for logging requests and response
    at application terminal
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(request)
        return view_func(request, *view_args, **view_kwargs)


class RawDataMiddleware(MiddlewareMixin):
    """ Identify request via adding hash
        to meta info for each request.
    """
    def process_request(self, request):
        request.META['id'] = uuid4()
        return view_func(request, *view_args, **view_kwargs)



class IdentifyResponseMiddleware(MiddlewareMixin):
    """ Identify response via adding hash
        to meta info for each response.
    """
    def process_template_response(request, response):
        response.META['id'] = uuid4()
        return view_func(request, *view_args, **view_kwargs)
