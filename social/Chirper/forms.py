from django import forms
from .models import Chirp
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Email Address',
    }))

    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First Name',
    }))

    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last Name',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted small">Required. 150 characters or fewer letters, digits and @/./+/-/_ only.</span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul><li><span class="form-text text-muted small">Your password can\'t be too similiar to your other personal information.</span></li><li><span class="form-text text-muted small">Your password must contain at least 8 characters.</span></li><li><span class="form-text text-muted small">Your password cannot be a commonly-used password.</span></li><li><span class="form-text text-muted small">Your password can\'t be entirely numeric.</span></li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted small">Enter the same password as before, for verfication.</span>'
