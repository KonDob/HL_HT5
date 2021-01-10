from uuid import uuid4
import logging

from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):
    """ Class for logging requests and response
    at application terminal
    """

    def process_request(self, request):
        log_request = "Request is " + str(request)
        logging.warning(log_request)

    def process_response(self, request, response):
        log_response = "Response is " + str(response)
        logging.warning(log_response)
        return response


class RawDataMiddleware(MiddlewareMixin):
    """ Identify request via adding hash
        to meta info for each request.
    """
    def process_request(self, request):
        request.META['id'] = uuid4()
        logging.warning(request.META['id'])


class IdentifyResponseMiddleware(MiddlewareMixin):
    """ Identify response via adding hash
        to meta info for each response.
    """
    def process_response(self, request, response):
        response['id'] = uuid4()
        return response
