from django.http import HttpRequest


def next_context_processor(request: HttpRequest):
    if 'next' not in request.GET:
        return {}
    return {'next': request.GET['next']}
