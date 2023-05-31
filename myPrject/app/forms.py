from django import forms
from .models import Korisnik, Predmeti
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class KorisnikForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = Korisnik
#         fields = ['username', 'first_name', 'last_name',
#                   'email', 'password', 'role', 'status']

#     def clean_password(self):
#         password = make_password(self.cleaned_data['password'])
#         return password

class KorisnikForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Korisnik
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password', 'role', 'status']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        # hash the password after the validation
        cleaned_data['password'] = make_password(password)
        return cleaned_data


class PredmetiForm(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program', 'ects',
                  'sem_red', 'sem_izv', 'izborni']
