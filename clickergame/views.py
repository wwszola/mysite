from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin

from .forms import CreateRoomForm, EnterRoomForm
from .models import Room


class RoomAccessMixin:
    def get_room_pk(self):
        if hasattr(self, "object") and self.object:
            return self.object.pk
        return self.kwargs.get("pk")

    def grant_room_access(self):
        pk = self.get_room_pk()
        entered_rooms = self.request.session.setdefault("entered_rooms", list())
        if pk not in entered_rooms:
            entered_rooms.append(pk)
            self.request.session.modified = True

    def has_room_access(self):
        pk = self.get_room_pk()
        room = Room.objects.get(pk=pk)
        entered_rooms = self.request.session.setdefault("entered_rooms", list())
        return pk in entered_rooms or room.is_not_password_protected


class PlayView(RoomAccessMixin, DetailView):
    model = Room
    context_object_name = "room"
    template_name = "clickergame/play.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.has_room_access():
            return HttpResponseRedirect(reverse("clickergame:enter", kwargs={"pk": self.get_room_pk()}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CreateRoomView(RoomAccessMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = CreateRoomForm
    template_name = "clickergame/create_room.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.grant_room_access()
        return response


class EnterRoomView(RoomAccessMixin, FormMixin, TemplateResponseMixin, View):
    form_class = EnterRoomForm
    template_name = "clickergame/enter_room.html"

    def get_success_url(self):
        return reverse("clickergame:play", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Room, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.object.pk
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.has_room_access():
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_password_protected:
            return HttpResponseBadRequest(f"Room {self.object.name} may be entered without a password")
        form = self.get_form()
        form.requested_room = self.object
        if form.is_valid():
            self.grant_room_access()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
