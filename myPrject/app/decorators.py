from django.http import HttpResponseForbidden
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You must be an admin to access this page.')
    return _wrapped_view


def profesor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'prof':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You must be a profesor to access this page.')
    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'stu':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You must be a student to access this page.')
    return _wrapped_view
