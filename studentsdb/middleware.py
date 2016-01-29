from datetime import datetime

from django.http import HttpResponse
from bs4 import BeautifulSoup

from .settings import DEBUG


class RequestTimeMiddleware(object):
    """Display request time on a page"""

    def process_request(self, request):
        request.start_time = datetime.now()
        return None

    def process_response(self, request, response):
        # if our process_request was canceled somewhere within
        # middleware stack, we can not calculate request time
        if not hasattr(request, 'start_time'):
            return response

        # calculate request execution time
        request.end_time = datetime.now()
        #if 'text/html' in response.get('Content-Type', '') and DEBUG:
        #    response.write('<br />Request took: %s' % str(
        #        request.end_time - request.start_time))
            #soup = BeautifulSoup(str(response))
            #gen_time = soup.div("gen_time")
            #gen_time.string = 'test_00000000000000000'

            #print gen_time
            #response.write(gen_time)

        return response

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None
