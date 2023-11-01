import django.forms as forms

from .models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ["allowed_users"]
        widgets = {
            "password": forms.PasswordInput(),
        }


class EnterRoomForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
