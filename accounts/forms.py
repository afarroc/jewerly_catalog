from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            logger.warning(f"Registration attempt with existing email: {email}")
            raise ValidationError("This email is already in use.")
        return email

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username or Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']