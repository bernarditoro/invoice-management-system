from django.contrib.auth import get_user


def user_context_processor(request):
    return {} if "admin" in request.path else {"user": get_user(request)}
    