from django.contrib import messages
from django.shortcuts import redirect


def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_student:
            messages.error(request, "您還不是學生")
            return redirect("teachers:index")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
