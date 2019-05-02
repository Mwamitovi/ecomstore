# Handling SSL in Python

# __license__ = "Python"
# __copyright__ = "Copyright (C) 2007, Stephen Zabel"
# __author__ = "Stephen Zabel - sjzabel@gmail.com"
# __contributors__ = "Jay Parlar - parlar@gmail.com"

from django.conf import settings
from django.http import \
    HttpResponsePermanentRedirect, HttpRequest
from django.utils.deprecation import MiddlewareMixin


SSL = 'SSL'


class SSLRedirect(MiddlewareMixin):
    """ middleware class for handling redirects back and forth between secure
    and non-secure pages. Taken from: http://www.djangosnippets.org/snippets/880/
    """

    # noinspection PyUnusedLocal
    def process_view(self, request, view_func, view_args, view_kwargs):
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False
        if not secure == self._is_secure(request):
            return self._redirect(request, secure)

    @staticmethod
    def _is_secure(request):
        if request.is_secure():
            return True
        # Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
        return False

    @staticmethod
    def _redirect(request, secure):
        protocol = secure and "https" or "http"
        new_url = "%s://%s%s" % (protocol, HttpRequest.get_host(request), request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError(
                """Django can't perform a SSL redirect while maintaining POST data.
                Please structure your views so that redirects only occur during GETs."""
            )
        return HttpResponsePermanentRedirect(new_url)
