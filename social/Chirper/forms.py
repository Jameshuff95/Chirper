from django import forms
from .models import Chirp

class ChirpForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            # This will allow to push stuff to form fields
            attrs={
                "placeholder": "Enter Your Chirp!",
                "class":"form-control",
            }
        ),
        label="",
    )

    class Meta:
        model = Chirp
        exclude =("user",)