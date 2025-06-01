from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile




class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ChangeUserForm(UserChangeForm):    
    class Meta: 
        model = User            
        fields = ['username', 'first_name', 'last_name', 'email']


# forms.py (add these to your existing forms)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'image': forms.FileInput(attrs={'class': 'w-full'}),
        }


