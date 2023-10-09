from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseCreateView, DeletionMixin

from .forms import PersonalInfoForm


class RegisterView(SingleObjectTemplateResponseMixin, BaseCreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/register.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object:
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
        return response


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object:
            try:
                ctx["github_url"] = self.object.github_info.get_profile_url()
            except self.model.github_info.RelatedObjectDoesNotExist:
                pass
        return ctx


class ProfileUpdateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            self.object = request.user
            personal_info_form = PersonalInfoForm(instance=self.object)
            ctx = {
                "personal_info_form": personal_info_form,
            }
            return render(request, "accounts/profile_update.html", ctx)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = request.user
        personal_info_form = PersonalInfoForm(request.POST, instance=self.object)
        if personal_info_form.is_valid():
            self.object = personal_info_form.save()
            return HttpResponseRedirect(reverse("accounts:update"))
        else:
            ctx = {
                "personal_info_form": personal_info_form,
            }
            return render(request, "accounts/profile_update.html", ctx)


class AccountDeleteView(DeletionMixin, View):
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_object(self):
        return self.request.user
