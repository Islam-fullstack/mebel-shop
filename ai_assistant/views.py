from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import ChatSession, ChatMessage
from .services import chat_with_ai


def chat_view(request):
    if request.user.is_authenticated:
        session, _ = ChatSession.objects.get_or_create(user=request.user, defaults={})
    else:
        if not request.session.session_key:
            request.session.create()
        session, _ = ChatSession.objects.get_or_create(session_key=request.session.session_key)
    messages = session.messages.all()
    return render(request, 'ai_assistant/chat.html', {'messages': messages, 'session': session})


@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except (json.JSONDecodeError, AttributeError):
        user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({'error': 'Xabar bo\'sh'}, status=400)

    if request.user.is_authenticated:
        session, _ = ChatSession.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session, _ = ChatSession.objects.get_or_create(session_key=request.session.session_key)

    ChatMessage.objects.create(session=session, role='user', content=user_message)

    all_messages = list(session.messages.all())
    history = [{'role': m.role, 'content': m.content} for m in all_messages[:-1]]
    ai_response = chat_with_ai(history, user_message)

    ChatMessage.objects.create(session=session, role='assistant', content=ai_response)

    return JsonResponse({'response': ai_response, 'success': True})


@require_POST
def clear_chat(request):
    if request.user.is_authenticated:
        ChatSession.objects.filter(user=request.user).delete()
    else:
        session_key = request.session.session_key
        if session_key:
            ChatSession.objects.filter(session_key=session_key).delete()
    return JsonResponse({'success': True})