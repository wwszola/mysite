from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin

from .forms import CreateRoomForm, EnterRoomForm
from .models import Room


class PlayView(DetailView):
    model = Room
    context_object_name = "room"
    template_name = "clickergame/play.html"


class CreateRoomView(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = CreateRoomForm
    template_name = "clickergame/create_room.html"


class EnterRoomView(FormMixin, TemplateResponseMixin, View):
    form_class = EnterRoomForm
    template_name = "clickergame/enter_room.html"

    def get_success_url(self):
        return reverse("clickergame:play", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Room, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.object.id
        return context

    def dispatch(self, request, *args, **kwargs):
        # this only temporary, allow for anonymous/guest users after a Person model has been implemented
        if self.request.user.is_anonymous:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.password == "":
            self.object.allow_user(request.user)
            return HttpResponseRedirect(self.get_success_url())
        if self.object.is_user_allowed(request.user):
            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.password == "":
            self.object.allow_user(request.user)
            return HttpResponseRedirect(self.get_success_url())
        form = self.get_form()
        if form.is_valid():
            self.object.allow_user(request.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
