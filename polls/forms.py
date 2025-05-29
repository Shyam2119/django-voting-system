from django import forms
from .models import Vote, Election, Candidate

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect)
    
    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['candidate'].queryset = Candidate.objects.filter(election=election)