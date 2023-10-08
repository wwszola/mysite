import django.forms as forms

from .models import Message


class PostMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
