from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):

    def process_view(self):


class RawDataMiddleware(MiddlewareMixin):
    pass


class IdentifyResponseMiddleware(MiddlewareMixin):
    pass
