from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class EditUserForm(ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    #email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name') #'email', 

class EditProfileForm(ModelForm):
    major = forms.CharField(max_length=50, required=False)
    minor = forms.CharField(max_length=50, required=False)
    classes_taken = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    private = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Profile
        fields = ('major', 'minor', 'classes_taken', 'private')
