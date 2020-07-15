from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import profile

class RegisterForm(UserCreationForm):
       
       class Meta:
           model=User
           fields=['username','email','password1','password2']
           
      
class ProfileUpdateForm(forms.ModelForm):
      class Meta:
           model=profile
           fields=['image','bio']
		   
           
class LoginForm(AuthenticationForm):
     username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),label="username")
     password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),label="password")