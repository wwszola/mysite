from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import PostMessageForm
from .models import Message


class IndexChatView(ListView):
    template_name = "chat/index.html"

    def get_queryset(self):
        return Message.objects.order_by("-pub_datetime")


class PostMessageView(CreateView):
    form_class = PostMessageForm
    template_name = "chat/post.html"
    success_url = reverse_lazy("chat:index")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            message = form.instance
            if request.user.is_authenticated:
                message.user_author = request.user
            else:
                guest_no = int(datetime.now().strftime("%Y%m%d%H%M%S"))
                message.guest_author = f"guest{guest_no}"
            return self.form_valid(form)
        else:
            return self.form_invalid()
