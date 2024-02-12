from Flow.models import *
from django import forms
from django.shortcuts import render


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by', 'members', 'Likes', 'created_at')

class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['tag']


EVENT_TYPES = (
	('', '-----'),
	('conference', 'Conférence'),
	('workshop', 'Atelier'),
    ('meetup', 'Rencontre'),
    ('party', 'Soirée'),
    ('spectacle', 'Spectacle'),
    ('sport', 'Sport'),
    ('other', 'Autre'),
    )

class SearchForm(forms.Form):
    title = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'événement'})
    )
    date = forms.DateField(
        required = False,
        widget=forms.DateInput(attrs={'placeholder': 'Date (JJ/MM/AAAA)'})
    )
    tags = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'Tags'})
    )
    event_type = forms.ChoiceField(
        required=False, 
        widget = forms.Select, 
        choices = EVENT_TYPES
    )

    