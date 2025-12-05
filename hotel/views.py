from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class Hotel(View):
    def get(self, request):
        return HttpResponse("HELLO, CLOWN")

    def post(self, request):
        return HttpResponse("bb, doter")
