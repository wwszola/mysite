import django.forms as forms
from django.contrib.auth import hashers

from .models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ["admin_user"]
        widgets = {"password": forms.PasswordInput()}

    def clean_password(self):
        raw_password = self.cleaned_data.get("password", None)
        if raw_password is None:
            return None
        else:
            encoded = hashers.make_password(raw_password)
            return encoded
