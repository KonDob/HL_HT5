from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):

<<<<<<< HEAD
    def process_view(self):
=======
    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view')
        return view_func(request, *view_args, **view_kwargs)
>>>>>>> master


class RawDataMiddleware(MiddlewareMixin):
    pass


class IdentifyResponseMiddleware(MiddlewareMixin):
    pass
