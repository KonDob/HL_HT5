from uuid import uuid4

from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):
    """ Class for logging requests and response
    at application terminal
    """

    def process_request(self, request):
        req = "Request is " + str(request)
        print(req)

    def process_response(self, request, response):
        res = "Response is " + str(response)
        print(res)
        return response


class RawDataMiddleware(MiddlewareMixin):
    """ Identify request via adding hash
        to meta info for each request.
    """
    def process_request(self, request):
        request.META['id'] = uuid4()


class IdentifyResponseMiddleware(MiddlewareMixin):
    """ Identify response via adding hash
        to meta info for each response.
    """
    def process_response(self, request, response):
        response['id'] = uuid4()
        return response
