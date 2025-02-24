from django.shortcuts import redirect


def can_not_be_logged(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return func(request, *args, **kwargs)
    return wrapper
