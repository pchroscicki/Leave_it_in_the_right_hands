from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię', 'required': True}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko', 'required': True}))
    username = forms.EmailField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Email', 'required': True}))
    password  = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło', 'required': True}))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło', 'required': True}))

    def clean_username(self):
        users = User.objects.filter(username=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise ValidationError("Podany email już jest zarejestrowany")

    def clean(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise ValidationError("Hasła nie są zgodne")


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password'
                  )

        def __init__(self, request, *args, **kwargs):
            super().init(*args, **kwargs)

            self.fields['first_name', 'last_name', 'username'].initial = request.user

        def clean_username(self):
            users = User.objects.filter(username=self.cleaned_data["username"])
            if not users:
                return self.cleaned_data["username"]
            raise ValidationError("Podany email już jest zarejestrowany")

