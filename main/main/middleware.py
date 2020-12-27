from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view')
        return view_func(request, *view_args, **view_kwargs)


class RawDataMiddleware(MiddlewareMixin):
    pass


class IdentifyResponseMiddleware(MiddlewareMixin):
    pass
