from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class IsActiveMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        pass
        #if not request.user.is_active:
            #logout(request)
            #return HttpResponseRedirect('/')