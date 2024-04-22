from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["text"]
        widgets = {
            "text": Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write something!"
            })
        }