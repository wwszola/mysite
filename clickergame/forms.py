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

    requested_room: Room

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.requested_room.check_password(password):
            raise self.get_incorrect_password_error()
        return password

    def get_incorrect_password_error(self):
        return forms.ValidationError(
            "Incorrect password to room %(room_name)s", code="incorrect", params={"room_name": self.requested_room.name}
        )
