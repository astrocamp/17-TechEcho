from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from chat.forms.chat_form import ChatMessageForm
from chat.models import ChatGroup
from editors.utils.run_code import run_javascript_code, run_python_code
from lib.utils.pagination import paginate
from lib.utils.student_required import student_required


@login_required
def index(request):
    if request.POST:
        code = request.POST.get("code")
        language = request.POST.get("language")
        if language == "javascript":
            result = run_javascript_code(code)
        elif language == "python":
            result = run_python_code(code)
        else:
            return JsonResponse({"error": "Unsupported language"}, status=400)
        return JsonResponse({"result": result})

    if not ChatGroup.objects.filter(group_name="public_chat").exists():
        ChatGroup.objects.create(group_name="public_chat", is_public=True)
    chat_group = ChatGroup.objects.get(group_name="public_chat")

    chat_messages = chat_group.messages.select_related("author")
    chat_messages = paginate(request, chat_messages, items_count=30, default_page=-1)
    return render(
        request,
        "editors/index.html",
        {
            "form": ChatMessageForm(),
            "chat_messages": chat_messages,
            "chat_group_id": chat_group.id,
        },
    )
