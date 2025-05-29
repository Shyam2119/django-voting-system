# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    voter_id = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_voter_id(self):
        voter_id = self.cleaned_data['voter_id']
        if Profile.objects.filter(voter_id=voter_id).exists():
            raise ValidationError("A user with this voter ID already exists.")
        return voter_id

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=commit)
        
        if commit:
            # Get or create the profile (in case signal didn't create it)
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Update the profile with additional fields
            profile.voter_id = self.cleaned_data['voter_id']
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
            
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'voter_id', 'phone_number']

    def clean_voter_id(self):
        voter_id = self.cleaned_data['voter_id']
        # Check if another profile (not this one) has the same voter_id
        if Profile.objects.filter(voter_id=voter_id).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this voter ID already exists.")
        return voter_id