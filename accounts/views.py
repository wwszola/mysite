from django.views.generic import View, DetailView
from django.views.generic.edit import FormMixin

from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http import QueryDict

from .forms import PersonalInfoForm

class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object:
            ctx['github_url'] = self.object.github_info.get_profile_url()
        return ctx

class ProfileUpdateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            self.object = request.user
            personal_info_form = PersonalInfoForm(instance = self.object)
            ctx = {
                'personal_info_form': personal_info_form,
            }
            return render(request, 'profile_update.html', ctx)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = request.user
        personal_info_form = PersonalInfoForm(request.POST, instance = self.object)
        if personal_info_form.is_valid():
            self.object = personal_info_form.save()
            return HttpResponseRedirect(reverse('accounts:update'))
        else:
            ctx = {
                'personal_info_form': personal_info_form,
            }
            return render(request, 'profile_update.html', ctx)