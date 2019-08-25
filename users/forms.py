from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm): #inherting UserCreationForm
    email = forms.EmailField()
    class Meta:
        model = User 
        fields = ['username','email','password1','password2'] #adding this field to it
