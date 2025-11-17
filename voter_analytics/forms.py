# File: forms.py
# Author: Anna LaPrade (alaprade@bu.edu), 10/28/2025
# Description: forms for the voter_analytics app

from django import forms
from .models import Voter

# voter year and voter score rangers
YEARS = [(y, y) for y in range(1900, 2026)]
VOTER_SCORES = [(i, i) for i in range(1, 6)]

# build party choices based on data
party_choices = [('', 'Any')]
all_parties = Voter.objects.values_list('party_affiliation', flat=True)
unique_parties = sorted({p for p in all_parties if p}) 
party_choices = [('', 'Any')] + [(p, p) for p in unique_parties]


# form to faciliate filtering Voters
class VoterFilterForm(forms.Form):
    # drop down menu of party choices
    party_affiliation = forms.ChoiceField(
        required=False,
        choices=party_choices,
        label="Party"
    )

    # drop down menus for max and min dates of birth (year)
    min_dob = forms.ChoiceField(required=False, choices=[('', 'Any')] + YEARS, label="Min Year of Birth")
    max_dob = forms.ChoiceField(required=False, choices=[('', 'Any')] + YEARS, label="Max Year of Birth")
    
    # voter score drop down
    voter_score = forms.ChoiceField(required=False, choices=[('', 'Any')] + VOTER_SCORES, label="Voter Score")
    
    # elections voted in check menu
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town")