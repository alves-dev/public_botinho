from django.views.decorators.csrf import csrf_exempt
import core.utils as u
from django.http.response import HttpResponse


@csrf_exempt
def event(requests):
    u.trata_conversa(requests)
    return HttpResponse()
