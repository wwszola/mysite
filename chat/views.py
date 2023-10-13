import json
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View

from .models import Message


class ReadMessagesPartialView(View):
    def get(self, request, length):
        message_list = list(Message.objects.order_by("-pub_datetime")[:length])
        html = render_to_string("chat/read_messages_snippet.html", context={"message_list": message_list})
        return HttpResponse(html)


class PostMessageView(View):
    def post(self, request):
        is_request_ajax = request.headers.get("X-Requested-With", None) == "XMLHttpRequest"
        if is_request_ajax:
            body = json.loads(request.body)
            content = body.get("content", None)
        else:
            content = request.POST.get("content", None)
        if content is None or len(content) == 0:
            return HttpResponse("no content", status=400)
        message = Message(content=content)
        if request.user.is_authenticated:
            message.user_author = request.user
        else:
            guest_no = int(datetime.now().strftime("%Y%m%d%H%M%S"))
            message.guest_author = f"guest{guest_no}"
        message.save()
        return HttpResponse(status=201)
