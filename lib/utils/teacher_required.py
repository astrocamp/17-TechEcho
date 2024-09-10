from django.contrib import messages
from django.shortcuts import redirect


def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, "您還不是老師")
            return redirect("teachers:mentor")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
