from django import forms
from ogidni.models import Story
from django.contrib.auth.models import User

class StoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ['name', 'text', 'genre']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
