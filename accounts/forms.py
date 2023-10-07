import django.forms as forms
from django.contrib.auth import get_user_model


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
