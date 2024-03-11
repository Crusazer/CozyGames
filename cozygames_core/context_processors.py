from django.http import HttpRequest


def next_context_processor(request: HttpRequest):
    print("\033[33mINFO:\033[0m point in next_context_processor")
    if 'next' not in request.GET:
        return {}
    return {'next': request.GET['next']}
