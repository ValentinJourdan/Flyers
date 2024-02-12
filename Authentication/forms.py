from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    pseudo = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('pseudo',)
        labels = {
            'username': 'Adresse électronique',
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Adresse électronique', widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = User
        fields = ('email', 'password')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        # Ajoutez ici les champs supplémentaires nécessaires pour le producteur
        fields = ['email', 'avatar']

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['name', 'avatar']