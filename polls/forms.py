from django import forms

from .models import Event, Fighter, Match


class EventForm(forms.ModelForm):
    choices = [
        ('Open', 'Open'),
        ('Closed', 'Closed')
    ]
    poll_status = forms.ChoiceField(choices=choices, initial='Closed')

    class Meta:
        model = Event
        fields = [
            'name',
            'poll_status',
            'date',
        ]


class FighterForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label=None)

    class Meta:
        model = Fighter
        fields = [
            'image',
            'first_name',
            'last_name',
            'weight',
            'gym',
            'event',
        ]


class MatchForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label=None)
    red_corner = forms.ModelChoiceField(queryset=Fighter.objects.all(), empty_label=None)
    blue_corner = forms.ModelChoiceField(queryset=Fighter.objects.all(), empty_label=None)

    class Meta:
        model = Match
        fields = [
            'event',
            'red_corner',
            'blue_corner',
        ]


class VoteMatchForm(forms.ModelForm):
    votes = forms.ModelChoiceField(queryset=Match.objects.all(), widget=forms.RadioSelect, empty_label=None)

    class Meta:
        model = Match
        fields = [
            'votes',
        ]


