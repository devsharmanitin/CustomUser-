from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser
from django import forms






class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','username')
        
        
class CustomUserRegisterForm(forms.ModelForm):
    confPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('username' , 'email' , 'password')
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),   
        }
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email','username')
        