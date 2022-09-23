from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię', 'required': True}))
    last_name = forms.CharField(max_length=64,
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko', 'required': True}))
    email = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': True}))
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło', 'required': True}))
    password2 = forms.CharField(max_length=30,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło', 'required': True}))

    def clean(self):
        data = super().clean()
        users = User.objects.filter(email=data["email"])
        if not users:
            if data["password"] != data["password2"]:
                raise ValidationError("Hasła nie są zgodne")
        else:
            raise ValidationError("Podany email jest już zarejestrowany")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class ContactForm(forms.Form):
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Temat'}))
    from_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Twój email'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Wiadomość'}))
